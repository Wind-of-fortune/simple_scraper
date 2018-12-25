# -*- coding: utf-8 -*-
import re
import time
import csv

import requests as rq

from secret_url import url_1, url_2, url_3, url_4, url_5


def getting_list_obj(teg, text, res=100):
    try:
        res = '{,' + str(res) + '}'
        teg_2 = '</' + teg[1:]
        r = re.findall(teg + '.' + res + teg_2, text)  # not here
        obj = []
        for i in r:
            o = i.replace(teg, '')
            o = o.replace(teg_2, '')
            obj.append(o)

        new_obj = []
        for i in range(len(obj)):
            if i == 0:
                new_obj.append(obj[i])
            if i > 0:
                if obj[i] != obj[i - 1]:
                    new_obj.append(obj[i])
        return new_obj
    except Exception:
        return None


def cutter(teg, text, res=100, item=0):
    try:
        res = '.{0,' + str(res) + '}'
        teg_2 = '</' + teg[1:]
        r = re.findall(teg + res + teg_2, text)[item]  # not here
        r = r.replace(teg, '')
        r = r.replace(teg_2, '')
        return r
    except Exception:
        return None


# PART_1 - collecting id's
r = rq.get(url_1)
data = r.json()
all_id = []

for i in data:
    for key, val in i.items():
        if key == 'id' and val != '0':
            all_id.append(val)

all_links = {}

for i in all_id:
    new_url = url_2.format(i, i)
    r = rq.get(new_url)

    data = re.findall(r'<gkId>\d{10}</gkId>', r.text)
    num_collect = []
    for k in data:
        num = k.replace('<gkId>', '')
        num = num.replace('</gkId>', '')
        num_collect.append(num)
    if type(num_collect) is list and len(num_collect) > 0:
        all_links[i] = num_collect

f = csv.writer(open("new_flats_all.csv", "w+"))

f.writerow(['main_name', 'main_id', 'object_name', 'build_group_type', 'region', 'town', 'street',
            'brand', 'rating', 'place', 'builder', 'state', 'begin_plan', 'end_plan', 'build_class', 'floors',
            'living_square', 'trim_type', 'build_material', 'all_apartment_count', 'sell_apartment_count',
            'money_org'
            ])

# PART_2 - paginate id's
for key, val in all_links.items():
    for i in val:
        try:
            main_url = url_3.format(i, key)

            try:
                r = rq.get(main_url)
            except Exception:
                time.sleep(10)
                r = rq.get(main_url)

            main_name = cutter('<name>', r.text, res=50, item=-1)
            main_id = i

            find_ids_url = url_4.format(i, i, key)

            try:
                r = rq.get(find_ids_url)
            except Exception:
                time.sleep(10)
                r = rq.get(main_url)

            obj_names = getting_list_obj('<objectName>', r.text)
            obj_urls = getting_list_obj('<objectId>', r.text, res=10)

            counter = 0
            for o in obj_urls:

                obj_link = url_5.format(o, key)
                try:
                    r = rq.get(obj_link)
                except Exception:
                    time.sleep(10)
                    r = rq.get(obj_link)

                o_name = obj_names[counter]

                counter += 1

                build_group_type = cutter('<buildType>', r.text)
                region = cutter('<region>', r.text)
                adress = cutter('<address>', r.text, res=200)
                organization_name = cutter('<organizationName>', r.text, res=200)
                developer_name = cutter('<developerName>', r.text, res=200)
                state = cutter('<phase>', r.text)
                rating = cutter('<ratingErz>', r.text)
                place = cutter('<place>', r.text)
                town = cutter('<place>', r.text, item=-1)
                begin_plan = cutter('<beginPlan>', r.text)
                end_plan = cutter('<endPlan>', r.text)
                build_class = cutter('<buildClass>', r.text)
                floors = cutter('<floorTo>', r.text, res=10)
                living_square = cutter('<livingSquare>', r.text)
                trim_type = cutter('<trimType>', r.text)
                build_material = cutter('<buildMaterial>', r.text)
                all_apartment_count = cutter('<allApartmentCount>', r.text)
                sell_apartment_count = cutter('<sellApartmentCount>', r.text)
                money_org = cutter('<moneyOrg>', r.text)

                # PART_3 write data to csv file
                try:
                    try:
                        k = int(place)
                    except Exception:
                        place = None

                    f.writerow(
                        [main_name, main_id, o_name, build_group_type, region,
                         town, adress, organization_name, rating, place,
                         developer_name, state, begin_plan, end_plan, build_class,
                         floors, living_square, trim_type, build_material, all_apartment_count,
                         sell_apartment_count, money_org
                         ])
                except Exception:
                    pass
                time.sleep(0.5)
        except Exception:
            pass


