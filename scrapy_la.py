import os
import re
from argparse import ArgumentParser

import pandas as pd
from scrapinghub import ScrapinghubClient

TYPE_OF_ERRORS_PATTERN = re.compile('(?<=\[)(.+)(?=\])', re.DOTALL)
DESCRIPTION_PATTERN = re.compile('(?<=\])\s(.+?)((?=<)|(?=\(URL)|(?=,))', re.DOTALL)
URL_PATTERN = re.compile('((?<=\(URL:)|(?<=for url: \')|(?<=GET)|(?<=POST))(.+?)((?=>)|(?=,)|(?=\'))', re.DOTALL)
RESPONSE_URL_PATTERN = re.compile('(?<=response URL:)(.+?)(?=\))', re.DOTALL)
PYTHON_MESSAGE_OF_ERROR_PATTERN = re.compile('(?<=Traceback \(most recent call last\))(.+)', re.DOTALL)


def parse_args():
    parent_parser = ArgumentParser(add_help=False)
    parent_parser.add_argument(
        '-a',
        '--apikey',
        help='Scrapinghub API'
    )
    parent_parser.add_argument(
        'job',
        help='Job key in format project_id/spider_id/job_id'
    )
    parser = ArgumentParser(
        description='Get statistic for scrapy log',
        parents=[parent_parser]
    )
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_errors = subparsers.add_parser(
        'errors',
        help='Analyze log errors',
    )
    parser_errors.add_argument(
        '-m',
        '--max',
        type=int,
        help='Set max urls to output for each error',
        default=3,

    )

    parser_errors.set_defaults(func=parse_errors)
    parser_warnings = subparsers.add_parser(
        'warnings',
        help='Analyze log warnings',
    )
    parser_warnings.set_defaults(func=parse_warnings)
    return parser.parse_args()


def get_part_of_log_with_re(re_compile, message):
    try:
        return re_compile.search(message).group(0).strip()
    except Exception:
        return


def get_python_message_of_error(re_compile, message, only_type=False):
    desc = get_part_of_log_with_re(re_compile, message)
    if not desc:
        return
    desc = desc.split('\n')
    try:
        if only_type:
            return re.search('(.+)(?=:)', desc[-1]).group(0).strip()
        else:
            return desc[-1].strip()
    except Exception:
        return


def get_python_type_of_error(re_compile, message):
    return get_python_message_of_error(re_compile, message, only_type=True)


def parse_warnings(job, urls_for_output=3):
    print("Parsing logs with warnings in progress...")


def create_errors_header(df):
    return "\n".join([
        "Errors in the log: {}".format(df.shape[0]),
        "With different scrapy types: {}".format(df.scrapy_type.unique().size),
        "With different description: {}".format(df.description.unique().size),
        "With different url: {}".format(df.url.unique().size),
        "With different response_url: {}".format(df.response_url.unique().size),
        "With different python types of errors: {}".format(
            df.python_type.unique().size
        ),
        "With different python messages: {}".format(
            df.python_message.unique().size
        ),
        "--------- Part for code debugging -----------"
        ])


def create_errors_body(df_grouped, max_urls_for_output):
    comment_template = '    # {} ({} from {} different {})'
    urls_template = '    "{}",'
    body = ["test_urls = ["]

    for (desc, group) in df_grouped:
        body.append(comment_template.format(
            desc,
            max_urls_for_output,
            group.shape[0],
            group['url'].unique().size)
        )
        for url in list(group.groupby(['url']).groups)[:max_urls_for_output]:
            body.append(urls_template.format(url))

    body.append("]")
    return "\n".join(body)


def parse_errors(job, max_urls_for_output=3):
    handlers = {
        'scrapy_type':
            [get_part_of_log_with_re, TYPE_OF_ERRORS_PATTERN],
        'description':
            [get_part_of_log_with_re, DESCRIPTION_PATTERN],
        'url':
            [get_part_of_log_with_re, URL_PATTERN],
        'response_url':
            [get_part_of_log_with_re, RESPONSE_URL_PATTERN],
        'python_type':
            [get_python_type_of_error, PYTHON_MESSAGE_OF_ERROR_PATTERN],
        'python_message':
            [get_python_message_of_error, PYTHON_MESSAGE_OF_ERROR_PATTERN]
    }

    raw_errors_list = job.logs.list(level='ERROR')
    errors = []
    for error in raw_errors_list:
        message = error.get('message', '')
        error_dict = dict()
        for key, handler in handlers.items():
            error_dict[key] = handler[0](handler[1], message)
        errors.append(error_dict)

    df = pd.DataFrame(errors)
    header = create_errors_header(pd.DataFrame(errors))
    print(header)

    df_grouped = df.groupby(['description'], as_index=False)
    body = create_errors_body(df_grouped, max_urls_for_output)

    print(body)


def main():
    args = parse_args()
    apikey = os.environ.get('SH_APIKEY') or args.apikey
    if not apikey:
        print('Please set API key')
        exit(1)

    client = ScrapinghubClient(apikey)
    job = client.get_job(args.job)
    args.func(job, max_urls_for_output=(min(args.max, 30)))


if __name__ == '__main__':
    main()
