# Automated Farming Systems - afs_fastapi

## Project Outline

### 1. Project Purpose
This project aims to harness Machine Learning (ML) and robotics to automate essential farming processes, including operating farm equipment, maintaining soil health, and managing water quality. By integrating data-driven insights with advanced automation, the project seeks to enhance farming efficiency, sustainability, and productivity.

The system provides a robust set of API interfaces, using [FastAPI](https://fastapi.tiangolo.com), to support diverse use cases, ranging from controlling robotic devices and physical farm equipment to monitoring environmental factors such as soil, water, and air quality. The APIs are designed to serve a wide range of consumers, including AI agents managing autonomous operations and humans overseeing the overall system or specific subsystems.

---

### 2. Locating Operational Manuals for Farm Equipment

**Objective:** Identify and utilize online resources that provide operational manuals for farm equipment. These manuals will guide the adaptation of current robotics to operate agricultural machines for automation purposes.

**Sources:**
1. [AgManuals](https://agmanuals.com)
2. [Case IH Operator Manuals](https://www.caseih.com/en-us/unitedstates/service-support/operators-manuals)
3. [Farm Manuals Fast](https://farmmanualsfast.com)
4. [AGCO Technical Publications](https://www.agcopubs.com)
5. [John Deere Manuals and Training](https://www.deere.com/en/parts-and-service/manuals-and-training)
6. [Farming and Construction Manuals](https://farming-constructionmanuals.com)
7. [Solano Horizonte](https://solano-horizonte.com/download-catalogs-and-manuals-of-agricultural-machinery)
8. [Yesterday's Tractors Forums](https://forums.yesterdaystractors.com)
9. [Tractor Tools Direct](https://tractortoolsdirect.com/manuals)
10. [General Implement Distributors](https://www.generalimp.com/manuals)

---

### 3. Monitoring and Maintaining Soil Conditions

**Objective:** Research and utilize tools, sensors, and platforms to monitor soil composition, mineral content, and pH balance, ensuring optimal crop health.

**Resources:**
1. [Soil Scout](https://soilscout.com)
2. [Renke 4-in-1 Soil Nutrient Sensor](https://www.renkeer.com/product/soil-nutrient-sensor/)
3. [Murata Soil Sensors](https://www.murata.com/en-us/products/sensor/soil)
4. [HORIBA LAQUAtwin pH Meters](https://www.horiba.com/usa/water-quality/applications/agriculture-crop-science/soil-ph-and-nutrient-availability/)
5. [Sensoterra Soil Moisture Sensors](https://www.sensoterra.com/soil-sensor-for-agriculture/)
6. [DFRobot 4-in-1 Soil Sensor](https://www.dfrobot.com/product-2830.html)
7. [EarthScout Agricultural Field Sensors](https://www.earthscout.com/)
8. [University of Minnesota Extension: Soil Moisture Sensors](https://extension.umn.edu/irrigation/soil-moisture-sensors-irrigation-scheduling)
9. [ATTRA: Soil Moisture Monitoring Tools](https://attra.ncat.org/publication/soil-moisture-monitoring-low-cost-tools-and-methods/)
10. [ESCATEC Electrochemical Sensors](https://www.escatec.com/blog/electrochemical-sensors-soil-analysis-through-precision-agriculture)

---

### 4. Monitoring and Maintaining Water Conditions

**Objective:** Identify and deploy tools to assess and maintain water composition, mineral levels, and pH balance, ensuring water quality is optimized for agricultural use.

**Resources:**
1. [Renke Water Quality Sensors](https://www.renkeer.com/top-7-water-quality-sensors/)
2. [In-Situ Agriculture Water Monitoring](https://in-situ.com/us/agriculture)
3. [Xylem Analytics Water Quality Monitoring](https://www.xylemanalytics.com/en/products/water-quality-monitoring)
4. [KETOS Automated Water Monitoring](https://ketos.co/)
5. [YSI Water Quality Systems](https://www.ysi.com/products)
6. [SGS Agricultural Water Testing](https://www.sgs.com/en-us/services/agricultural-water-testing)
7. [Boqu Instrument Water Quality Sensors](https://www.boquinstrument.com/how-water-quality-sensors-are-used-in-agriculture-and-farming.html)
8. [Digital Matter Remote Sensor Solutions](https://sense.digitalmatter.com/blog/water-quality-monitoring)
9. [Intuz IoT Water Monitoring](https://www.intuz.com/blog/iot-for-water-monitoring-in-crops)
10. [Rika Sensor Water Quality Sensors](https://www.rikasensor.com/blog-top-10-water-quality-sensors-for-water-treatments.html)

---

### 5. Utilizing Publicly Available Water Sampling Datasets

**Objective:** Access and analyze publicly available water quality datasets to inform ML models for monitoring water conditions suitable for farming.

**Sources:**
1. [Water Quality Portal (WQP)](https://www.waterqualitydata.us/)
2. [USGS National Water Information System (NWIS)](https://catalog.data.gov/dataset)
3. [EPA Water Quality Data](https://www.epa.gov/waterdata/water-quality-data)
4. [Kaggle: Water Quality Dataset for Crop](https://www.kaggle.com/datasets/abhishekkhanna004/water-quality-dataset-for-crop)
5. [Ag Data Commons: Soil and Water Hub Modeling](https://agdatacommons.nal.usda.gov/articles/dataset/Soil_and_Water_Hub_Modeling_Datasets/24852681)
6. [NASA Earthdata: Water Quality](https://www.earthdata.nasa.gov/topics/ocean/water-quality)

---

### 6. Project Integration and Machine Learning Goals

**Objective:** Synthesize the research and datasets into ML models and robotics systems capable of automating farm operations, improving efficiency, and ensuring sustainability. Models will address:
- Autonomous machine operation (leveraging operational manuals).
- Soil condition predictions and adjustments.
- Water quality monitoring and real-time management.

**Tools and Techniques:**
- ML libraries like TensorFlow and PyTorch.
- IoT-enabled sensors for real-time data collection.
- Integration with cloud platforms for data storage and analysis.

---

### Conclusion
This project will employ cutting-edge ML and robotics solutions to automate farming processes, ensuring optimized resource utilization and sustainable agricultural practices.

## Project Setup
The project uses the following:

- Python 3.11 or 3.12. The project has _not_ been tested with Python 3.13
- fastAPI
- pydantic
- requests
- uvicorn

For testing/development the project adds the following packages. Uninstall them, if you wish, for production.

- black
- factory-boy|factory_boy
- Faker
- flake8
- isort
- pytest
- pytest-bdd
- pytest-mock
- rich

While most folks won't put it directly there, the worldview is from a user's ``$HOME`` directory.

It is recommended that you use a Python virtual environment for this project, which can be set up as follows. The 2 most popular ways are Python 3.x's ``-m venv`` and miniconda's ``conda``. Use only *one* of them! The project is actively developed using miniconda to control the environment. 

However, the second way of using ``python -m venv`` is included for those not using miniconda, but instead are using ``python3`` and ``pip``. 

Both share use of the ``deactivate`` command to exit the respective virtual environment, so don't forget to call it when done. 

Please note, the listing of installed packages for both approaches is shown simply for a baseline.

#### miniconda/conda way

```zsh
(base)
user@machine ~ % git clone https://github.com/dderyldowney/afs_fastapi.git
<git output will display as it clones repo>

(base)
user@machine ~ % cd afs_fastapi

(base)
user@machine ~/afs_fastapi % conda env create -f conda-environment.yml
<lots of conda output>

(base)
user@machine ~/afs_fastapi % conda activate afs_fastapi

(afs_fastapi)
user@machine ~/afs_fastapi % conda list
# packages in environment at /opt/miniconda3/envs/afs_fastapi:
#
# Name                    Version                   Build  Channel
annotated-types           0.7.0              pyhd8ed1ab_1    conda-forge
anyio                     4.4.0              pyhd8ed1ab_0    conda-forge
black                     24.10.0         py312hb401068_0    conda-forge
brotli-python             1.0.9           py312h6d0c2b6_9
bzip2                     1.0.8                hfdf4475_7    conda-forge
ca-certificates           2024.12.31           hecd8cb5_0
certifi                   2024.12.14      py312hecd8cb5_0
charset-normalizer        3.3.2              pyhd3eb1b0_0
click                     8.1.8              pyh707e725_0    conda-forge
colorama                  0.4.6              pyhd8ed1ab_1    conda-forge
dnspython                 2.7.0              pyhff2d567_1    conda-forge
email-validator           2.2.0              pyhd8ed1ab_1    conda-forge
email_validator           2.2.0                hd8ed1ab_1    conda-forge
exceptiongroup            1.2.2              pyhd8ed1ab_1    conda-forge
factory_boy               3.2.0           py312hecd8cb5_0
faker                     30.8.1          py312hecd8cb5_0
fastapi                   0.115.6            pyhd8ed1ab_0    conda-forge
fastapi-cli               0.0.7              pyhd8ed1ab_0    conda-forge
flake8                    7.1.1              pyhd8ed1ab_1    conda-forge
h11                       0.14.0             pyhd8ed1ab_1    conda-forge
h2                        4.1.0              pyhd8ed1ab_1    conda-forge
hpack                     4.0.0              pyhd8ed1ab_1    conda-forge
httpcore                  1.0.7              pyh29332c3_1    conda-forge
httptools                 0.6.4           py312h01d7ebd_0    conda-forge
httpx                     0.28.1             pyhd8ed1ab_0    conda-forge
hyperframe                6.0.1              pyhd8ed1ab_1    conda-forge
idna                      3.10               pyhd8ed1ab_1    conda-forge
iniconfig                 2.0.0              pyhd8ed1ab_1    conda-forge
isort                     5.13.2             pyhd8ed1ab_1    conda-forge
jinja2                    3.1.5              pyhd8ed1ab_0    conda-forge
libcxx                    14.0.6               h9765a3e_0
libexpat                  2.6.4                h240833e_0    conda-forge
libffi                    3.4.2                h0d85af4_5    conda-forge
liblzma                   5.6.3                hd471939_1    conda-forge
libsqlite                 3.48.0               hdb6dae5_0    conda-forge
libuv                     1.48.0               h67532ce_0    conda-forge
libzlib                   1.3.1                hd23fc13_2    conda-forge
mako                      1.2.3           py312hecd8cb5_0
markdown-it-py            3.0.0              pyhd8ed1ab_1    conda-forge
markupsafe                3.0.2           py312h3520af0_1    conda-forge
mccabe                    0.7.0              pyhd8ed1ab_1    conda-forge
mdurl                     0.1.2              pyhd8ed1ab_1    conda-forge
mypy_extensions           1.0.0              pyha770c72_1    conda-forge
ncurses                   6.5                  h0622a9a_2    conda-forge
openssl                   3.4.0                hc426f3f_1    conda-forge
packaging                 24.2               pyhd8ed1ab_2    conda-forge
parse                     1.19.1          py312hecd8cb5_0
parse_type                0.6.2           py312hecd8cb5_0
pathspec                  0.12.1             pyhd8ed1ab_1    conda-forge
pip                       24.3.1             pyh8b19718_2    conda-forge
platformdirs              4.3.6              pyhd8ed1ab_1    conda-forge
pluggy                    1.5.0              pyhd8ed1ab_1    conda-forge
pycodestyle               2.12.1             pyhd8ed1ab_1    conda-forge
pydantic                  2.10.5             pyh3cfb1c2_0    conda-forge
pydantic-core             2.27.2          py312h0d0de52_0    conda-forge
pyflakes                  3.2.0              pyhd8ed1ab_1    conda-forge
pygments                  2.19.1             pyhd8ed1ab_0    conda-forge
pysocks                   1.7.1           py312hecd8cb5_0
pytest                    8.3.4              pyhd8ed1ab_1    conda-forge
pytest-bdd                7.0.0           py312hecd8cb5_0
pytest-mock               3.14.0          py312hecd8cb5_0
python                    3.12.8          h9ccd52b_1_cpython    conda-forge
python-dateutil           2.9.0post0      py312hecd8cb5_2
python-dotenv             1.0.1              pyhd8ed1ab_1    conda-forge
python-multipart          0.0.20             pyhff2d567_0    conda-forge
python_abi                3.12                    5_cp312    conda-forge
pyyaml                    6.0.2           py312hb553811_1    conda-forge
readline                  8.2                  h9e318b2_1    conda-forge
requests                  2.32.3          py312hecd8cb5_1
rich                      13.9.4          py312hecd8cb5_0
rich-toolkit              0.11.3             pyh29332c3_0    conda-forge
setuptools                75.8.0             pyhff2d567_0    conda-forge
shellingham               1.5.4              pyhd8ed1ab_1    conda-forge
six                       1.16.0             pyhd3eb1b0_1
sniffio                   1.3.1              pyhd8ed1ab_1    conda-forge
starlette                 0.41.3             pyha770c72_1    conda-forge
tk                        8.6.13               h1abcd95_1    conda-forge
tomli                     2.2.1              pyhd8ed1ab_1    conda-forge
typer                     0.15.1             pyhd8ed1ab_0    conda-forge
typer-slim                0.15.1             pyhd8ed1ab_0    conda-forge
typer-slim-standard       0.15.1               hd8ed1ab_0    conda-forge
typing-extensions         4.12.2               hd8ed1ab_1    conda-forge
typing_extensions         4.12.2             pyha770c72_1    conda-forge
tzdata                    2025a                h78e105d_0    conda-forge
urllib3                   2.3.0           py312hecd8cb5_0
uvicorn                   0.34.0             pyh31011fe_0    conda-forge
uvicorn-standard          0.34.0               h31011fe_0    conda-forge
uvloop                    0.20.0          py312hb553811_0    conda-forge
watchfiles                1.0.4           py312h0d0de52_0    conda-forge
websockets                14.1            py312h01d7ebd_0    conda-forge
wheel                     0.45.1             pyhd8ed1ab_1    conda-forge
yaml                      0.2.5                h0d85af4_2    conda-forge

(afs_fastapi)
user@machine ~/afs_fastapi % 
```

#### Python 3.x venv module way
```zsh
user@machine ~ % git clone https://github.com/dderyldowney/afs_fastapi.git
<git output will display as it clones repo>

user@machine ~ % cd afs_fastapi
 
user@machine ~ % python -V
Python 3.12.8

user@machine ~/afs_fastapi % python -m venv --prompt afs_fastapi .venv
<bunch of output from python>

user@machine ~/afs_fastapi % source .venv/bin/activate

(afs_fastapi)
user@machine ~/afs_fastapi % pip install -r pip-environment.txt
<bunch of output from pip>

(afs_fastapi)
user@machine ~/afs_fastapi % pip list
Package            Version
------------------ -----------
annotated-types    0.7.0
anyio              4.4.0
black              24.10.0
Brotli             1.0.9
certifi            2024.12.14
charset-normalizer 3.3.2
click              8.1.8
colorama           0.4.6
dnspython          2.7.0
email_validator    2.2.0
exceptiongroup     1.2.2
factory-boy        3.2.0
Faker              30.8.1
fastapi            0.115.6
fastapi-cli        0.0.7
flake8             7.1.1
h11                0.14.0
h2                 4.1.0
hpack              4.0.0
httpcore           1.0.7
httptools          0.6.4
httpx              0.28.1
hyperframe         6.0.1
idna               3.10
iniconfig          2.0.0
isort              5.13.2
Jinja2             3.1.5
Mako               1.2.3
markdown-it-py     3.0.0
MarkupSafe         3.0.2
mccabe             0.7.0
mdurl              0.1.2
mypy_extensions    1.0.0
packaging          24.2
parse              1.19.1
parse-type         0.6.2
pathspec           0.12.1
pip                24.3.1
platformdirs       4.3.6
pluggy             1.5.0
pycodestyle        2.12.1
pydantic           2.10.5
pydantic_core      2.27.2
pyflakes           3.2.0
Pygments           2.19.1
PySocks            1.7.1
pytest             8.3.4
pytest-bdd         7.0.0
pytest-mock        3.14.0
python-dateutil    2.9.0.post0
python-dotenv      1.0.1
python-multipart   0.0.20
PyYAML             6.0.2
requests           2.32.3
rich               13.9.4
rich-toolkit       0.11.3
setuptools         75.8.0
shellingham        1.5.4
six                1.16.0
sniffio            1.3.1
starlette          0.41.3
tomli              2.2.1
typer              0.15.1
typer-slim         0.15.1
typing_extensions  4.12.2
urllib3            2.3.0
uvicorn            0.34.0
uvloop             0.20.0
watchfiles         1.0.4
websockets         14.1
wheel              0.45.1

(afs_fastapi)
user@machine ~/afs_fastapi % 
```
Your output should be exactly like the list above. When you're done working with the project, don't forget to do a ``deactivate`` to unload the virtual environment.

Reloading the environment again is as simple as changing to the project directory and executing: ``source ./venv/bin/activate``
