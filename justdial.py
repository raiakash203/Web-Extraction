from SeleniumScraping import *
from bs4 import BeautifulSoup


logging.basicConfig(filename="JustDialScraping.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":

    driver = SeleniumDriver("E:\\JustDialScrapper\\chromedriver.exe")
    logger.info('Driver Object created')
    url = 'https://www.justdial.com/'
    query = 'Restaurants in Janakpuri District Center'
    location = "Delhi"
    outputFile = query.replace(' ', '_')+'.csv'
    driver.getUrl(url)
    logger.info('Driver Object calls getUrl function with url "{}"'.format(url))
    driver.setLocation(location)
    logger.info('Driver Object set location "{}"'.format(location))
    check = driver.searchItem(query)
    logger.info('Driver Object sets query "{}"'.format(query))
    links = list()
    alreadyLinks = list()
    df = pd.DataFrame(columns=['Name', 'Ratings', 'Votes', 'Address'])

    try:
        x = check.find_elements_by_xpath('//*[@id="srchpagination"]/a')
        for i in x:
            item = i.get_attribute('href')
            if item:
                if item not in links and item not in alreadyLinks:
                    links.append(item)
            else:
                continue
        link = links.pop(0)
        alreadyLinks.append(link)
        check.get(link)
        driver.scrollpage()
    except Exception as e:
        print(e)
        logger.error(' Error:  {}'.format(e))

    while len(links) != 0:
        logger.info('Scraping for following Url  "{}"'.format(link))
        soup = BeautifulSoup(check.page_source, "lxml")
        services = soup.find_all('li', {'class': 'cntanr'})
        logger.info("All services for this page is being extracted")
        for service_html in services:
            # Parse HTML to fetch data
            dict_service = {}
            name = get_name(service_html)
            phone = get_phone_number(service_html)
            rating = get_rating(service_html)
            count = get_rating_count(service_html)
            address = get_address(service_html)
            location = get_location(service_html)
            df.loc[len(df)] = [name, rating, count, address]

        try:
            # WebDriverWait(check, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="srchpagination"]/a[11]')))
            x = check.find_elements_by_xpath('//*[@id="srchpagination"]/a')
            for i in x:
                item = i.get_attribute('href')
                if item:
                    if item not in links and item not in alreadyLinks:
                        links.append(item)
                else:
                    continue

            link = links.pop(0)
            alreadyLinks.append(link)
            check.get(link)
            driver.scrollpage()
        except Exception as e:
            logger.error(' Error:  {}'.format(e))

    df.drop_duplicates(inplace=True)
    df.to_csv(outputFile, sep='|', encoding='utf-8', mode='a', index=False)
    logger.info("Output file with name '{}' is created".format(outputFile))
    check.close()