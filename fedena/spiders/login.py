import scrapy
import time

class LoginSpider(scrapy.Spider):
    name = 'fedena'
    start_urls = ['http://10.1.131.10:8080']

    def parse(self, response):
        username = input("Enter Username:").strip()
        password = input("Enter Password:").strip()
        return scrapy.FormRequest.from_response(
            response,
            formdata={'user[username]': username, 'user[password]': password},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if str.encode("Invalid username or password combination") in response.body:
            self.logger.error("Login failed")
            print("\nIncorrect credentials\n")
            return
        else: #Logged in Whoohooo
            print("\n\n LOGGED IN, BC!!! \n")
            return scrapy.Request(url="http://10.1.131.10:8080/user/dashboard/", callback=self.get_grade_page_link)

    def get_grade_page_link(self, response):
        print("Scraping Fedena\n\n")
        links = response.css('p font a::attr(href)').extract()
        grade_link = [x for x in links if 'grade_sheet' in x][0]
        print("GOT THE GRADE PAGE LINK\n\n")

        grade_sheet_link = grade_link + "&year_sem=2016-17-2"
        print("GOT THE GRADE SHEET LINK\n\n")

        return scrapy.Request(url=grade_sheet_link, callback=self.download_the_sheet)
    def download_the_sheet(self, response):
        if str.encode("SPI") in response.body:
            print("GOTCHHA\n\n")
            print("DOWNLOADING.. \n\n")
            filename = "2016-17-1.html"
            with open(filename, 'wb') as f:
                f.write(response.body)

            print("Check file %s in fedena folder\n\n" %filename)
        else:
            print("\n\nNAHI AYA, BC :(\n\n")
            print("Retrying in 10 seconds.. (press Ctrl+C to stop the process)\n\n")
            time.sleep(10)
            return scrapy.Request(url=response.url, callback=self.download_the_sheet)
