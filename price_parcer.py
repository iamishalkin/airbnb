#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:26:47 2017

@author: ivan
"""


import requests
import json
import pandas as pd

BASE='https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty&_limit=18&sort=1&locale=ru-RU'
price_range=[300,400,500,600,700,800,900,950,1000,1050,1100,
             1150,1200,1250,1300,1350,1400,1450,1500,1550,1600,
             1650,1700,1750,1800,1850,1900,1950,2000,2100,2200,
             2300,2400,2500,2600,2700,2800,2900,3000,3100,3200,
             3300,3400,3500,3600,3700,4000,5000,6000,7000,8000,
             13000,15000]

while True:
    city=input('Введите город, как в airbnb (Samara--Samara-Oblast--Russia): ')
    city_short=city[0:city.find('--')]
    APARTMENTS=[] #this dataframe will be converted to csv
    REVIEWS=[]
    
    for idx, price in enumerate(price_range):
        price_min=price_range[idx]
        if idx == len(price_range)-1:
            break
        price_max=price_range[1+idx]
        print(price_min,price_max)
        
        
        for page in range(20):
            url=BASE + '&_offset='+str(page*50)+'&location=' + city +'&_limit=50'+'&price_min=' +str(price_min)+'&price_max='+str(price_max)
            jsonpage = json.loads(requests.get(url).text)
            if jsonpage.get('search_results')==[]:
                break
            else:
                observ=jsonpage.get('search_results')
                
            for i in range(len(observ)):
                idf=observ[i].get('listing') #get each listing
                listing_url='https://api.airbnb.com/v2/listings/'+str(idf.get('id'))+'?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3&locale=ru-RU'
                
                listing_jsonpage = json.loads(requests.get(listing_url).text)
                ftrs=listing_jsonpage.get('listing')
                amen=ftrs.get('amenities_ids')
                APARTMENTS.append({
                    "apart_id":idf.get('id'),
                    'apart_name': ftrs.get('name'),
                    'description':ftrs.get('summary'),#description
                    #'amenities':ftrs.get('amenities'),#udobstva need to be extended with amenities_ids
                    'bathrooms':ftrs.get('bathrooms'),
                    'bed_type':ftrs.get('bed_type'),#probably need ftrs.get('bed_type_category')
                    'bedrooms':ftrs.get('bedrooms'),
                    'beds':ftrs.get('beds'),
                    'cancellation_policy':ftrs.get('cancellation_policy'),           
                    #'check_in_time_start':ftrs.get('check_in_time_start'), #time when you are allowed to check in
                    #'check_out_time':ftrs.get('check_out_time'),
                    'city':ftrs.get('city'),
                    'cleaning_fee_native':ftrs.get('cleaning_fee_native'),
                    'country':ftrs.get('counntry'),#ftrs.get('country_code')
                    'description':ftrs.get('description'),
                    'extra_user_info':ftrs.get('extra_user_info'),
                    'extra_price_native':ftrs.get('extra_price_native'),
                    'guests_included':ftrs.get('guests_included'),
                    'has_agreed_to_legal_terms':ftrs.get('has_agreed_to_legal_terms'),
                    #'has_license':ftrs.get('has_license'),
                    'host_id':ftrs.get('hosts')[0].get('id'),
                    'house_rules':ftrs.get('house_rules'),
                    'in_building':ftrs.get('in_building'),
                    'instant_bookable':ftrs.get('instant_bookable'),
                    'interaction':ftrs.get('interaction'),#about hosts
                    'is_location_exact':ftrs.get('is_location_exact'),
                    'lat':ftrs.get('lat'),
                    'lng':ftrs.get('lng'),
                    #'listing_native_currency':ftrs.get('listing_native_currency'),
                    #'listing_cleaning_fee_native':ftrs.get('listing_cleaning_fee_native'),
                    #'listing_price_for_extra_person_native':ftrs.get('listing_price_for_extra_person_native'),
                    'max_nights':ftrs.get('max_nights'),
                    'min_nights':ftrs.get('min_nights'),
                    'monthly_price_factor':ftrs.get('monthly_price_factor'),
                    'native_currency':ftrs.get('native_currency'),
                    'neighborhood':ftrs.get('neighborhood'),#region
                    'neighborhood_overview':ftrs.get('neighborhood'),#region description
                    'notes':ftrs.get('notes'),#small description, some notes
                    'person_capacity':ftrs.get('person_capacity'),
                    'photo_url':ftrs.get('medium-url'),#.str.replace(u'?aki_policy=medium', ''),
                    'picture_count':ftrs.get('picture_count'),
                    'price_native':ftrs.get('price_native'),
                    'price_for_extra_person_native':ftrs.get('price_for_extra_person_native'),
                    'property_type':ftrs.get('property_type'),
                    'require_guest_phone_verification':ftrs.get('require_guest_phone_verification'),
                    'review_rating_accuracy':ftrs.get('review_rating_accuracy'),
                    'review_rating_checkin':ftrs.get('review_rating_checkin'),
                    'review_rating_cleanliness':ftrs.get('review_rating_cleanliness'),
                    'review_rating_communication':ftrs.get('review_rating_communication'),
                    'review_rating_location':ftrs.get('review_rating_location'),
                    'review_rating_value':ftrs.get('review_rating_value'),
                    'reviews_count':ftrs.get('reviews_count'),
                    'room_type':ftrs.get('room_type'),
                    'room_type_category':ftrs.get('room_type_category'),
                    'space':ftrs.get('space'),
                    #'special_offer':ftrs.get('special_offer'),
                    'square_feet':ftrs.get('square_feet'),
                    'star_rating':ftrs.get('star_rating'),
                    #'time_zone_name':ftrs.get('time_zone_name'),
                    #'toto_opt_in':ftrs.get('toto_opt_in'),
                    'transit':ftrs.get('transit'),
                    'weekly_price_factor':ftrs.get('weekly_price_factor'),
                    "Kitchen":8 in amen, #',"Кухня"
                    "Internet":3 in amen, #',"Интернет"
                    "TV":1 in amen, #',"Телевизор"
                    "Essentials":40 in amen, #',"Туалетные принадлежности"
                    "Shampoo":41 in amen, #',"Шампунь"
                    "Heating":30 in amen, #',"Отопление"
                    "Air_conditioning":5 in amen, #',"Кондиционер"
                    "Washer":33 in amen, #',"Стиральная машина"
                    "Dryer":34 in amen, #',"Сушильная машина"
                    "Free_parking_on_premises":9 in amen, #',"Бесплатная парковка"
                    "Free_parking_on_street":23 in amen, #',"Бесплатная парковка на улице"
                    "Paid_parking_off_premises":10 in amen, #',"Платная парковка рядом"
                    "Wireless_Internet":4 in amen, #',"Беспроводной Интернет"
                    "Cable_TV":2 in amen, #',"Кабельное телевидение"
                    "Breakfast":16 in amen, #',"Завтрак"
                    "Pets_allowed":12 in amen, #',"Можно с питомцами"
                    "Family_kid_friendly":31 in amen, #',"Подходит для детей/семей"
                    "Suitable_for_events":32 in amen, #',"Подходит для проведения мероприятий"
                    "Smoking_allowed":11 in amen, #',"Можно курить"
                    "Wheelchair_accessible":6 in amen, #',"Подходит людям с ограниченными возможностями"
                    "Elevator_in_building":21 in amen, #',"Лифт"
                    "Indoor_fireplace":27 in amen, #',"Камин"
                    "Buzzer_wireless_intercom":28 in amen, #',"Домофон"
                    "Doorman":14 in amen, #',"Вахтер"
                    "Pool":7 in amen, #',"Бассейн"
                    "Hot_tub":25 in amen, #',"Джакузи"
                    "Gym":15 in amen, #',"Спортзал"
                    "Hangers":44 in amen, #',"Плечики"
                    "Iron":46 in amen, #',"Утюг"
                    "Hair_dryer":45 in amen, #',"Фен"
                    "Laptop_friendly_workspace":47 in amen, #',"Место для работы на ноутбуке"
                    "Smoke_detector":35 in amen, #',"Пожарная сигнализация"
                    "Carbon_monoxide_detector":36 in amen, #',"Детектор угарного газа"
                    "First_aid_kit":37 in amen, #',"Аптечка"
                    "Safety_card":38 in amen, #',"Памятка по безопасности"
                    "Fire_extinguisher":39 in amen, #',"Огнетушитель"
                    "Lock_on_bedroom_door":42 in amen, #',"Замок на двери в спальню"
                    "Self_Check_In":51 in amen, #',"Самостоятельное прибытие"
                    'url': 'https://www.airbnb.com/rooms/'+str(idf.get('id'))
                    })
                    
                if ftrs.get('reviews_count') == 0:
                    #has no reviews
                    continue
                else:
                    #has some
                    print('listing has some reviews')
                    revurl='https://api.airbnb.com/v2/reviews?client_id=3092nxybyb0otqw18e8nh5nty&listing_id=' + str(idf.get('id'))+'&role=all'
                    json_review_page = json.loads(requests.get(revurl).text)
                    revs=json_review_page.get('reviews')#list with review dicts
                    #print(revurl)
                    for g in range(len(revs)):
                        revdict=revs[g]
                        REVIEWS.append({
                            'apart_id':idf.get('id'),
                            'author_id':revdict.get('author_id'),
                            'date':revdict.get('created_at'),
                            'review':revdict.get('comments')
                            })
                        fd=pd.DataFrame(REVIEWS)
                
                        fd.to_csv('reviews/Review_'+city_short+'.csv' , header=True, index=False, encoding='utf-8')
                        
                df = pd.DataFrame(APARTMENTS)
                
                df.to_csv('apartments/'+city_short+'.csv' , header=True, index=False, encoding='utf-8')

    print(city_short, ' collected')        
