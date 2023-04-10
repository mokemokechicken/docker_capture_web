"""
Thanks
======
https://github.com/mrcoles/full-page-screen-capture-chrome-extension/blob/master/page.js
"""

from argparse import ArgumentParser
from collections import namedtuple
from io import BytesIO
from logging import CRITICAL, DEBUG, INFO, basicConfig, getLogger
from time import sleep

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ClientInfo = namedtuple(
    "ClientInfo", "full_width full_height window_width window_height"
)
logger = getLogger(__name__)


def args_parser():
    parser = ArgumentParser()
    parser.add_argument("url", help="specify URL")
    parser.add_argument("filename", help="specify capture image filename")
    parser.add_argument(
        "-w", help="specify window size like 1200x800", dest="window_size", type=str
    )
    parser.add_argument("--ua", help="specify user-agent", dest="user_agent", type=str)
    parser.add_argument(
        "--wait",
        help="specify wait seconds after scroll",
        dest="wait",
        type=float,
        default=0.2,
    )
    parser.add_argument(
        "-v", help="set LogLevel to INFO", dest="log_info", action="store_true"
    )
    parser.add_argument(
        "--vv", help="set LogLevel to DEBUG", dest="log_debug", action="store_true"
    )
    return parser


def main():
    parser = args_parser()
    args = parser.parse_args()
    if args.window_size:
        window_size = [int(x) for x in args.window_size.split("x")]
    else:
        window_size = (1200, 800)

    if args.log_info:
        log_level = INFO
    elif args.log_debug:
        log_level = DEBUG
    else:
        log_level = CRITICAL
    basicConfig(
        level=log_level, format="%(asctime)s@%(name)s %(levelname)s # %(message)s"
    )

    capture_full_screenshot(
        args.url,
        args.filename,
        window_size=window_size,
        user_agent=args.user_agent,
        wait=args.wait,
    )


def capture_full_screenshot(
    url, filename, window_size=None, user_agent=None, wait=None
):
    """

    :param url:
    :param filename:
    :param None|tuple window_size: browser window size. tuple of (width, height)
    :param None|str user_agent:
    :param None|float wait:
    :return:
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    desired_capabilities = dict(acceptInsecureCerts=True)
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(
        options=options, desired_capabilities=desired_capabilities
    )

    if window_size:
        options.add_argument(f"window-size={window_size[0]},{window_size[1]}")

    driver.get(url)
    prepare_capture(driver)
    client_info = get_client_info(driver)

    ua = driver.execute_script("return navigator.userAgent")
    logger.info((client_info, ua))
    capture_screen_area(driver, filename, client_info, wait=wait)
    driver.close()


def capture_screen_area(
    driver: webdriver.Chrome, filename, client_info: ClientInfo, wait
):
    for y_pos in range(0, client_info.full_height - client_info.window_height, 300):
        scroll_to(driver, 0, y_pos)
        sleep(wait or 0.2)

    client_info = get_client_info(driver)

    y_pos = client_info.full_height - client_info.window_height
    x_delta = client_info.window_width
    y_delta = client_info.window_height - 200

    canvas = Image.new("RGB", (client_info.full_width, client_info.full_height))
    while y_pos > -y_delta:
        x_pos = 0
        while x_pos < client_info.full_width:
            scroll_to(driver, x_pos, y_pos)
            sleep(wait or 0.2)
            cur_x, cur_y = get_current_pos(driver)
            logger.info(
                f"scrolling to {(x_pos, y_pos)}, current pos is {(cur_x, cur_y)}"
            )
            img = Image.open(
                BytesIO(driver.get_screenshot_as_png())
            )  # type: Image.Image
            resized_image = img.resize(
                (client_info.window_width, client_info.window_height)
            )
            canvas.paste(resized_image, (cur_x, cur_y))
            img.close()
            resized_image.close()
            x_pos += x_delta
        y_pos -= y_delta
    canvas.save(filename)


def prepare_capture(driver):
    driver.execute_script(
        """
        document.body.style.overflowY = 'visible';
        // document.documentElement.style.overflow = 'hidden';
    """
    )


def get_client_info(driver):
    return ClientInfo(*driver.execute_script(FULL_SIZE_JS))


FULL_SIZE_JS = """
function max(nums) {
    return Math.max.apply(Math, nums.filter(function(x) { return x; }));
}

return [
    max([
            document.documentElement.clientWidth,
            document.body ? document.body.scrollWidth : 0,
            document.documentElement.scrollWidth,
            document.body ? document.body.offsetWidth : 0,
            document.documentElement.offsetWidth
    ]),
    max([
            document.documentElement.clientHeight,
            document.body ? document.body.scrollHeight : 0,
            document.documentElement.scrollHeight,
            document.body ? document.body.offsetHeight : 0,
            document.documentElement.offsetHeight
    ]),
    window.innerWidth,
    window.innerHeight
    ];
"""


def scroll_to(driver, x, y):
    driver.execute_script("window.scrollTo.apply(null, arguments)", x, y)


def get_current_pos(driver):
    return driver.execute_script("return [window.scrollX, window.scrollY]")


if __name__ == "__main__":
    main()
