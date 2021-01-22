from kni import KNI

kni = KNI('demo.school.kiwi')
notices = kni.retrieve('01/01/2020')
for notice in notices.notices:
    print(notice)