import logging
logging.basicConfig(level=logging.DEBUG, filename="general.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(module)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
# logging.error("An ERROR",exc_info=(stack_info=)
logging.critical("A message of CRITICAL severity")