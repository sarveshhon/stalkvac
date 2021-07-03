import time
from datetime import date

import requests
from playsound import playsound

BASE_URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?'
VACCINES = ['COVAXIN', 'COVISHIELD']
DOSE = ['available_capacity_dose1', 'available_capacity_dose2']
AGE = [18, 45]

VACCINE_CHOICE = 0  # Choose any Vaccine ( 0 -> COVAXIN, 1 -> COVISHIELD)

AGE_CHOICE = 0  # Choose any Age ( 0 -> 18Age, 1 - 45Age )

DOSE_CHOICE = 0  # Choose any Dose ( 0 -> 1st Dose, 1 -> 2nd Dose )


def fetchData(mDistrict, mDate):
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('district_id', mDistrict),
        ('date', mDate),
    )
    response = requests.get(BASE_URL, headers=headers, params=params)
    cleanData(response.json())


def cleanData(response):
    if (0 <= VACCINE_CHOICE < len(VACCINES)) and (0 <= DOSE_CHOICE < len(DOSE)) and (
            0 <= AGE_CHOICE < len(AGE)):
        for l in response['sessions']:
            if l['vaccine'] == VACCINES[VACCINE_CHOICE] and l['min_age_limit'] == AGE[AGE_CHOICE]:
                if DOSE[DOSE_CHOICE] == 'available_capacity_dose1':
                    if l['available_capacity_dose1'] > 0:
                        playAlert()
                        printLink()
                        info = l['vaccine'], l['pincode'], l['available_capacity_dose1'], l['min_age_limit'], l['name'], \
                               l['address']
                        print(info, end='\n')
                elif DOSE[DOSE_CHOICE] == 'available_capacity_dose2':
                    if l['available_capacity_dose2'] > 0:
                        playAlert()
                        printLink()
                        info = l['vaccine'], l['pincode'], l['available_capacity_dose2'], l['min_age_limit'], l['name'], \
                               l['address']
                        print(info, end='\n')
    else:
        print('Wrong Choice')


def playAlert():
    playsound('vaccine-available.mp3')


def printLink():
    print('https://selfregistration.cowin.gov.in/')


if __name__ == '__main__':
    while True:
        fetchData('391', date.today().strftime('%d-%m-%y'))
        print('Live Tracking')
        time.sleep(10)
