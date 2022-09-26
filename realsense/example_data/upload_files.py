files = """
2022-09-25_d415_and_d435/d415/2022-09-25_16-52-05_color.png
2022-09-25_d415_and_d435/d415/2022-09-25_16-52-05_depth.png
2022-09-25_d415_and_d435/d415/2022-09-25_16-52-05_pcd.pcd
2022-09-25_d415_and_d435/d415/extrinsics.json
2022-09-25_d415_and_d435/d415/metadata.json
2022-09-25_d415_and_d435/d435/2022-09-25_16-49-10_color.png
2022-09-25_d415_and_d435/d435/2022-09-25_16-49-10_depth.png
2022-09-25_d415_and_d435/d435/2022-09-25_16-49-10_pcd.pcd
2022-09-25_d415_and_d435/d435/extrinsics.json
2022-09-25_d415_and_d435/d435/metadata.json"""[1:].split("\n")

from ml_logger import logger

logger.configure("geyang/fast_nerf/depth-data")
logger.job_started()

logger.log_text("""
charts:
- type: image
  glob: "**/*.png"
""", ".charts.yml", True, True)

for f in files:
    logger.upload_file(f, f)
    print(f'{f} has been uploaded')

print(logger)
logger.job_completed()
