import json
from statistics import quantiles
from Model.GeographicalData.District import District
from Model.GeographicalData.Subprefecture import Subprefecture

class ObservaSampaReader:
    def __init__(self, mongo_db):
        self.file_path = "data/ObservaSampaDadosAbertosIndicadoresJSON.json"

        self.useful_flood_data_names = [
            "11.05.03 Número de ocorrências atendidas – inundação",
            "Número de ocorrências atendidas – alagamento",
            "11.05.09 Áreas de risco hidrológico na cidade de São Paulo (m²)"
        ]

        self.useful_population_data_names = [
            "População total",
            "População com 60 anos ou mais",
            "População com 15 anos ou mais"
        ]

        self.mongo_db = mongo_db
        self.regions_data = {}

    def get_region(self, name):
        if name not in self.regions_data:
            self.regions_data[name] = {
                "Populacao": {},
                "Alagamentos": {},
                "AnosInformacoes": []
            }

        return self.regions_data[name]

    def read_flood_data(self):
        data = self.read_data("flood", self.useful_flood_data_names)

        if data == []:
            return

        for d in data:
            region = d["Regiao"]
            region_record = self.get_region(region)

            name = d["NomeIndicador"]
            result = d["ResultadoIndicador"]

            self.add_year(region_record, int(d["Periodo"]))

            if name == self.useful_flood_data_names[0]:
                region_record["Alagamentos"]["CasosInundacao"] = result
            elif name == self.useful_flood_data_names[1]:
                region_record["Alagamentos"]["CasosAlagamento"] = result
            elif name == self.useful_flood_data_names[2]:
                region_record["Alagamentos"]["AreaRiscoHidrologico"] = result

            floods = region_record["Alagamentos"]

            if "CasosInundacao" in floods and "CasosAlagamento" in floods:
                floods["CasosTotais"] = floods["CasosInundacao"] + floods["CasosAlagamento"]

    def read_population_data(self):
        data = self.read_data("population", self.useful_population_data_names)

        if data == []:
            return

        for d in data:
            region = d["Regiao"]
            region_record = self.get_region(region)

            name = d["NomeIndicador"]
            result = d["ResultadoIndicador"]

            self.add_year(region_record, int(d["Periodo"]))

            if name == self.useful_population_data_names[0]:
                region_record["Populacao"]["Total"] = result
            elif name == self.useful_population_data_names[1]:
                region_record["Populacao"]["Idosos"] = result
            elif name == self.useful_population_data_names[2]:
                region_record["Populacao"]["AcimaDe15Anos"] = result

            population = region_record["Populacao"]

            if "Total" in population and "AcimaDe15Anos" in population:
                population["Criancas"] = population["Total"] - population["AcimaDe15Anos"]

    def read_all_data(self):
        self.read_flood_data()
        self.read_population_data()

        districts = []
        risks = []

        for region, d in self.regions_data.items():
            if not region.endswith("(Distrito)"):
                continue

            floods = d["Alagamentos"]
            population = d["Populacao"]

            risk = self.calculate_hydrological_risk(floods["CasosTotais"], population["Total"])

            districts.append({
                "nome": region.replace(" (Distrito)", ""),
                "populacao": population["Total"],
                "populacao_idosa": population["Idosos"],
                "populacao_criancas": population["Criancas"],
                "casos_alagamentos": floods["CasosTotais"],
                "risco_hidrologico": round(risk, 2),
                "anos_informacoes": d["AnosInformacoes"]
            })

            risks.append(risk)

        for region, d in self.regions_data.items():
            if not region.endswith("(Subprefeitura)"):
                continue

            floods = d["Alagamentos"]

            subprefecture = Subprefecture(
                nome=region.replace(" (Subprefeitura)", ""),
                area_risco_hidrologico=floods["AreaRiscoHidrologico"],
                anos_informacoes=d["AnosInformacoes"]
            )

            self.mongo_db.insert_subprefecture(subprefecture)

        self.define_hydrological_risk(districts)

    def define_hydrological_risk(self, districts):
        if not districts:
            return

        risks = [d["risco_hidrologico"] for d in districts]
        l1, l2, l3 = quantiles(risks, n=4, method="inclusive")

        for d in districts:
            risk = d["risco_hidrologico"]

            if risk <= l1:
                level = "Muito Baixo"
            elif risk <= l2:
                level = "Baixo"
            elif risk <= l3:
                level = "Moderado"
            else:
                level = "Alto"

            district = District(
                **d,
                nivel_risco_hidrologico=level
            )

            self.mongo_db.insert_district(district)

    def read_data(self, data_type: str, useful_data_names):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            records = {}

            for d in data:
                region = d["Regiao"]
                year = int(d["Periodo"])
                name = d["NomeIndicador"]

                if name not in useful_data_names:
                    continue

                if data_type == "flood":
                    if name != useful_data_names[2] and not region.endswith("(Distrito)"):
                        continue
                    elif name == useful_data_names[2] and not region.endswith("(Subprefeitura)"):
                        continue
                elif data_type == "population":
                    if not region.endswith("(Distrito)"):
                        continue

                if year < 2023:
                    continue

                key = (name, region)
                saved_data = records.get(key)

                if saved_data is None or year > int(saved_data["Periodo"]):
                    records[key] = d

            useful_data = [
                {
                    "NomeIndicador": record["NomeIndicador"],
                    "Regiao": record["Regiao"],
                    "Periodo": record["Periodo"],
                    "ResultadoIndicador": record["ResultadoIndicador"]
                }
                for record in records.values()
            ]

            return useful_data
        except Exception as e:
            print(f"Erro ao ler o arquivo JSON: {e}")
            return []

    @staticmethod
    def add_year(region_record, year):
        if year not in region_record["AnosInformacoes"]:
            region_record["AnosInformacoes"].append(year)

    @staticmethod
    def calculate_hydrological_risk(flood_cases, population):
        if population <= 0:
            return 0

        return (flood_cases / population) * 10000