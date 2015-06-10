from datetime import timedelta, date
import wget

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)

start_date = date(2011, 1, 1)
end_date = date(2012, 12, 31)

for current in daterange(start_date, end_date):
    current = {'day': current.day, 'month': current.month, 'year': current.year}
    url = 'http://water.weather.gov/precip/p_download_new/%(year)d/%(month)02d/%(day)02d/' % current
    url += 'nws_precip_%(year)d%(month)02d%(day)02d_nc.tar.gz' % current
    wget.download(url)
