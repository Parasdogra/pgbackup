from argparse import Action,ArgumentParser
known_drivers = ['local', 's3']

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string = None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error("unkown driver, available driver are local and s3")
        namespace.driver = driver.lower()
        namespace.destination = destination

def create_parser():
    parser = ArgumentParser()
    parser.add_argument("url", help="URL of the database to backup")
    parser.add_argument("--driver", "-d",
            help="how and where to store backup",
            nargs= 2,
            metavar=("DRIVER", "DESTINATION"),
            action = DriverAction,
            required=True)

    return parser

def main():
    import boto3
    import time
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)

    if args.driver == 's3':
        client = boto3.client('s3')

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        file_name = pgdump.dump_file_name(args.url, timestamp)
        print(f"Backing database up to {args.destination} in S3 as {file_name}")
        storage.s3(client, dump.stdout, args.destination, 'example.sql')

    else:
        outfile = open(args.destination, 'wb')
        print(f"Backing database up locally {args.destination}")
        storage.local(dump.stdout, outfile)


