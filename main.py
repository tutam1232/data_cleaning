import argparse
import asyncio
from suppliers.acme import AcmeSupplier 
from suppliers.patagonie import PatagonieSupplier
from suppliers.paperflies import PaperfliesSupplier

from services.hotel_services import sort_hotels, merge_hotels_list, print_hotels, output_hotels_to_json
from utils.utils import args_to_list, str_arr_to_int_arr
    
async def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("hotel_ids")
    parser.add_argument("destination_ids")
    args = parser.parse_args()
    hotel_ids = args_to_list(args.hotel_ids)
    destination_ids = str_arr_to_int_arr(args_to_list(args.destination_ids))


    # Fetch hotels and sanitize data
    all_hotels = []
    suppliers = [AcmeSupplier(), PaperfliesSupplier(), PatagonieSupplier()]
    for supplier in suppliers:
        fetched_hotels = await supplier.fetch(hotel_ids, destination_ids)
        parsed_hotels = supplier.parse(fetched_hotels)
        all_hotels.extend(parsed_hotels)

    # Sort and merge hotels
    sorted_hotels = sort_hotels(all_hotels, hotel_ids, destination_ids)
    merged_hotels = merge_hotels_list(sorted_hotels)

    # Output to json
    output_hotels_to_json(merged_hotels)



if __name__ == "__main__":
    asyncio.run(main())