import yaml
from src.Determine_Fame import setup, generate_artist_fame, name_similarity

with open(".project-metadata.yaml") as yaml_config:
    config = yaml.load(yaml_config, yaml.FullLoader)
if name_similarity(config["runtimes"][0]["dataset-existing"], "no"):
    setup()
    generate_artist_fame()