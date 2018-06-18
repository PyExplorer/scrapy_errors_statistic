import unittest

from scrapy_la import scrapy_la


class TestScrapyEs(unittest.TestCase):
    def test_get_scrapy_type_of_error(self):
        self.assertEqual(
            scrapy_la.get_part_of_log_with_re(
                scrapy_la.TYPE_OF_ERRORS_PATTERN,
                "[scrapy.core.scraper] Spider error processing <GET "
            ),
            "scrapy.core.scraper"
        )
        self.assertEqual(
            scrapy_la.get_part_of_log_with_re(
                scrapy_la.TYPE_OF_ERRORS_PATTERN,
                """
                [validation] Required item fields are missing 
                or empty ('url_product_page') for DiscoveryItem (URL)
                """
            ),
            "validation"
        )

    def test_get_description(self):
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.DESCRIPTION_PATTERN,
            "[scrapy.core.scraper] Spider error processing <GET "
            ),
            "Spider error processing"
        )
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.DESCRIPTION_PATTERN,
            """[validation] Required item fields are missing or
             empty ('url_product_page') for DiscoveryItem (URL
            """
            ),
            """Required item fields are missing or
             empty ('url_product_page') for DiscoveryItem"""
        )
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.DESCRIPTION_PATTERN,
            """[validation] Inconsistent 'products_on_page',
            page 1 from 'keywords_id' 'id79' was already found
            with a 'products_on_page' value of 16, and now is
            found with a value of 24 (URL:
            """
            ),
            "Inconsistent 'products_on_page'"
        )

    def test_get_url(self):
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.URL_PATTERN,
            """[validation] 
            value of 24 (URL: http://www.example.com/no7/no7-gift-with-purchase, 
            response URL: http://www.example.com/ref/no7-gift-with-purchase), 
            item dropped
            """
            ),
            "http://www.example.com/no7/no7-gift-with-purchase"
        )
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.URL_PATTERN,
            """Spider error processing 
            <GET https://www.example.com/product/examples.cfm> (referer: None)
            """
            ),
            "https://www.example.com/product/examples.cfm"
        )
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.URL_PATTERN,
            """Spider error processing 
            <POST https://www.example.com/product/examples.cfm> (referer: None)
            """
            ),
            "https://www.example.com/product/examples.cfm"
        )
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.URL_PATTERN,
            """[_keywords] duplicated field(s): 'page_item_number', 
            'page_number', 'keywords_id' (13, 1, 'id79') 
            for url: 'http://www.sample.com/no7-make-up/no7-mascaras'
            """
            ),
            "http://www.sample.com/no7-make-up/no7-mascaras"
        )
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.URL_PATTERN,
            """[brandview.middlewares.retry] Splash screenshot error 
            latency: 28.8296120167)
                {"url": "http://www.example.com/reeText=stainless+steel&srch=Y", 
                "reason": "network301", "message": "error rendering splash"}
            """
            ),
            "http://www.example.com/reeText=stainless+steel&srch=Y"
        )


    def test_get_response_url(self):
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.RESPONSE_URL_PATTERN,
            """[validation] value of 24 
            (URL: http://www.example.com/no7/no7-gift-with-purchase, 
            response URL: http://www.example.com/ref/no7-gift-with-purchase), 
            item dropped
            """
            ),
            "http://www.example.com/ref/no7-gift-with-purchase"
        )
        self.assertEqual(scrapy_la.get_part_of_log_with_re(
            scrapy_la.RESPONSE_URL_PATTERN,
            """Spider error processing 
            <POST https://www.example.com/product/examples.cfm> (referer: None)
            """
            ),
            None
        )

    def test_get_python_type_of_error(self):
        self.assertEqual(scrapy_la.get_python_type_of_error(
            scrapy_la.PYTHON_MESSAGE_OF_ERROR_PATTERN,
            """
              Traceback (most recent call last):
              File "/usr/local/lib/python2.7/site-packages/scrapy/utils
              /defer.py", line 102, in iter_errback
                yield next(it)
              File "/usr/local/lib/python2.7/site-packages/sh_scrapy
              /middlewares.py", line 30, in process_spider_output
                for x in result:
            TypeError: exceptions must be old- classes or ..., not NoneType"""
            ),
            "TypeError"
        )

    def test_get_python_all_message_of_error(self):
        self.assertEqual(scrapy_la.get_python_message_of_error(
            scrapy_la.PYTHON_MESSAGE_OF_ERROR_PATTERN,
            """
              Traceback (most recent call last):
              File "/usr/local/lib/python2.7/site-packages/scrapy/utils/
              defer.py", line 102, in iter_errback
                yield next(it)
              File "/usr/local/lib/python2.7/site-packages/sh_scrapy/
              middlewares.py", line 30, in process_spider_output
                for x in result:
            TypeError: exceptions must be old-style classes or ... not eType"""
            ),
            "TypeError: exceptions must be old-style classes or ... not eType"
        )


if __name__ == "__main__":
    unittest.main()

