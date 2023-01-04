#!/usr/bin/env bash

# change to the full path of where the Non_Interpretable_features folder is
cd '/export/afavaro/git_code_version/speech/Cross_Lingual_Evaluation/interpretable_features/'

#  Mono-Lingual experiments

# colombian

python nested_cross_validation/multi_lingual/colombian/AUROC/RP.py
python nested_cross_validation/multi_lingual/colombian/Models/RP.py
python nested_cross_validation/multi_lingual/colombian/SENS/RP.py

python nested_cross_validation/multi_lingual/colombian/AUROC/SS.py
python nested_cross_validation/multi_lingual/colombian/Models/SS.py
python nested_cross_validation/multi_lingual/colombian/SENS/SS.py

python nested_cross_validation/multi_lingual/colombian/AUROC/TDU.py
python nested_cross_validation/multi_lingual/colombian/Models/TDU.py
python nested_cross_validation/multi_lingual/colombian/SENS/SS.py

# czech

python nested_cross_validation/multi_lingual/czech/AUROC/RP.py
python nested_cross_validation/multi_lingual/czech/Models/RP.py
python nested_cross_validation/multi_lingual/czech/SENS/RP.py

python nested_cross_validation/multi_lingual/czech/AUROC/SS.py
python nested_cross_validation/multi_lingual/czech/Models/SS.py
python nested_cross_validation/multi_lingual/czech/SENS/SS.py

# American english

python nested_cross_validation/multi_lingual/english/AUROC/RP.py
python nested_cross_validation/multi_lingual/english/Models/RP.py
python nested_cross_validation/multi_lingual/english/SENS/RP.py

python nested_cross_validation/multi_lingual/english/AUROC/SS.py
python nested_cross_validation/multi_lingual/english/Models/SS.py
python nested_cross_validation/multi_lingual/english/SENS/SS.py


# german

python nested_cross_validation/multi_lingual/german/AUROC/RP.py
python nested_cross_validation/multi_lingual/german/Models/RP.py
python nested_cross_validation/multi_lingual/german/SENS/RP.py

python nested_cross_validation/multi_lingual/german/AUROC/SS.py
python nested_cross_validation/multi_lingual/german/Models/SS.py
python nested_cross_validation/multi_lingual/german/SENS/SS.py

python nested_cross_validation/multi_lingual/german/AUROC/TDU.py
python nested_cross_validation/multi_lingual/german/Models/TDU.py
python nested_cross_validation/multi_lingual/german/SENS/TDU.py


# italian

python nested_cross_validation/multi_lingual/italian/AUROC/RP.py
python nested_cross_validation/multi_lingual/italian/Models/RP.py
python nested_cross_validation/multi_lingual/italian/SENS/RP.py

python nested_cross_validation/multi_lingual/italian/AUROC/TDU.py
python nested_cross_validation/multi_lingual/italian/Models/TDU.py
python nested_cross_validation/multi_lingual/italian/SENS/TDU.py

# Castilian spanish

python nested_cross_validation/multi_lingual/spanish/AUROC/TDU.py
python nested_cross_validation/multi_lingual/spanish/Models/TDU.py
python nested_cross_validation/multi_lingual/spanish/SENS/SS.py

python nested_cross_validation/multi_lingual/spanish/AUROC/SS.py
python nested_cross_validation/multi_lingual/spanish/Models/SS.py
python nested_cross_validation/multi_lingual/spanish/SENS/SS.py