import os
import glob
from pydicom import dcmread


# manual:
# 1. put your files in ./dicom_files (there is a chance you may need to create it)
# 2. run anonymize.py
# 3. anonymized files are in ./out dir

dcm_root_dir = "./dicom_files/"

files_input_dir = glob.glob("**/**/*", recursive=True, root_dir=dcm_root_dir)

tags_and_fixed_anonymous_values = {
    "AccessionNumber": "0006669972137",
    "InstitutionAddress": "Addr",
    "InstitutionName": "Anonymus Institution",
    "OperatorsName": "Anonymous^Operator",
    "PatientID": "2137",
    "PatientName": "Anonymous^Patient",
    "PatientsBirthDate": "19200518",
    "OtherPatientIDs": "666",
    "ReferringPhysiciansName": "Anonymous^Referring^Physicians",
    "PhysiciansofRecord": "Anonymized",
    "PerformedProcedureStepDescription": "Anonymous Procedure Step Description",
    "PerformedProcedureStepID": "Anonymous Step ID",
    "PerformedProcedureStepStartDate": "20050402",
    "RequestingPhysician": "Anonymous^Requesting^Physician",
    "StudyID": "anonoymus_xxxx",
    "NameofPhysiciansReadingStudy": "Anonymous Physicians Reading Study",
}


def anonymize_single_dcm(file_path: str):
    f_p = os.path.join(dcm_root_dir, file_path)
    base_file_name = os.path.basename(f_p)
    ds = dcmread(f_p)

    out_dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "out", file_path)
    os.makedirs(out_dir_path, exist_ok=True)
    for key, val in tags_and_fixed_anonymous_values.items():
        if not key in ds:
            print('there is no', key, 'in the dicom')
            continue
        print(ds[key])
        ds[key].value = val
    ds.remove_private_tags()
    ds.save_as(os.path.join(out_dir_path, base_file_name))


for file_path in files_input_dir:
    f_p = os.path.join(dcm_root_dir, file_path)
    if os.path.isdir(f_p):
        continue
    anonymize_single_dcm(file_path)
