from src.app import TrackerApp
from src.scrapper import KayakScrapper
from src.utils import load_config, parse_args

if __name__ == "__main__":
    args = parse_args()
    if args.config is None:
        app = TrackerApp(args.timeout)
        app.run()
    else:
        cfg = load_config("./configs", args.config)
        tracker = KayakScrapper(cfg, args.timeout)
        possible_trips = tracker.scrape()
        print(possible_trips)
