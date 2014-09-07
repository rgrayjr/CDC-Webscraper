#!/usr/bin/env python
""" Match addresses against the CDC
website
"""
import csv
import requests
import re
from collections import defaultdict
from bs4 import BeautifulSoup

def get_info_on_webpage(url):
    """Get the addresses from the webpage"""
    soup = BeautifulSoup(requests.get(url).text)

    # Clean up <br/> tags
    for linebreak in soup.findAll('br'):
        linebreak.extract()

    info_sp = soup.findAll('table', id='resultwithin')

    organization_info = [['Name', 'Address', 'City', 'Zip', 'Phone']]

    for info in info_sp:
        org_name = info.find(id=re.compile("OrgLabelsHere")).text
        street = info.find(id=re.compile("Street1Label")).string
        city = info.find(id=re.compile("CityLabel")).string
        zipcode = info.find(id=re.compile("ZipCodeLabel")).string
        phone = info.find(id=re.compile("LbPhone")).parent.parent.findNext('td').text.strip()

        organization_info.append([org_name, street, city, zipcode, phone])

    return organization_info

def get_addresses_from_csv(csv_path):
    """write docstring"""
    columns_dict = defaultdict(list)

    with open(csv_path, 'rb') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            for (k, value) in row.items():
                columns_dict[k].append(value)

    return columns_dict['Address 1']

def normalize_address(address_list):
    """write docstring"""
    address_list = [address.upper() for address in address_list]

    address_list = [re.sub(r'  *', ' ', address) for address in address_list]
    address_list = [re.sub(r'\.', '', address) for address in address_list]
    address_list = [re.sub(r'\,', '', address) for address in address_list]

    address_list = [re.sub(r'(\s|^)AVE(\s+|$)', r'\1AVENUE\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)ST(\s+|$)', r'\1STREET\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)DR(\s+|$)', r'\1DRIVE\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)RD(\s+|$)', r'\1ROAD\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)PL(\s+|$)', r'\1PLACE\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)HWY(\s+|$)', r'\1HIGHWAY\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)BLVD(\s+|$)', r'\1BOULEVARD\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)RTE(\s+|$)', r'\1ROUTE\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)LN(\s+|$)', r'\1LANE\2', address)
                    for address in address_list]

    address_list = [re.sub(r'(\s|^)NW(\s+|$)', r'\1NORTHWEST\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)N(\s+|$)', r'\1NORTH\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)NE(\s+|$)', r'\1NORTHEAST\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)E(\s+|$)', r'\1EAST\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)SE(\s+|$)', r'\1SOUTHEAST\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)S(\s+|$)', r'\1SOUTH\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)SW(\s+|$)', r'\1SOUTHWEST\2', address)
                    for address in address_list]
    address_list = [re.sub(r'(\s|^)W(\s+|$)', r'\1WEST\2', address)
                    for address in address_list]

    return address_list

def sorted_nicely(mylist):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(mylist, key=alphanum_key)

def main():
    """docstring"""
    alabama_url = "http://hivtest.cdc.gov/Detail.aspx?id=19465&id=113040&id=12647&id=37135&id=113610&id=12651&id=112092&id=110287&id=12688&id=37132&id=12692&id=12696&id=37134&id=37133&id=22624&id=5912&id=37129&id=37126&id=626&id=30795&id=24168&id=19807&id=5092&id=12645&id=12660&id=12679&id=18631&id=12662&id=12673&id=12709&id=5044&id=12641&id=113656&id=113658&id=12663&id=12687&id=12697&id=12706&id=113657&id=12698&id=19825&id=22513&id=19824&id=12667&id=24201&id=12646&id=12666&id=12672&id=113607&id=12650&id=113611&id=12659&id=12670&id=12674&id=113612&id=12694&id=113614&id=12704&id=12707&id=19808&id=12708&id=12710&id=113608&id=22601&id=5090&id=113613&id=113609&id=113615&id=12675&id=12640&id=12695&id=3801&id=12637&id=12658&id=12668&id=12690&id=17752&id=37136&id=12643&id=12671&id=12683&id=37138&id=12648&id=37142&id=112521&id=19826&id=112517&id=37141&id=26339&id=111796&id=1789&id=15450&id=112515&id=112514&id=112520&id=23852&id=112516&id=111795&id=12699&id=19828&id=12644&id=12669&id=12678&id=12681&id=12689&id=12652&id=12700&id=12693&id=27982&id=112519&id=113067"

    webpage_addresses = [info[1]
                         for info in get_info_on_webpage(alabama_url)
                         if info[1] != 'Address']
    webpage_addresses = set(normalize_address(webpage_addresses))
    csv_addresses = get_addresses_from_csv("csv/Alabama.csv")
    csv_addresses = set(normalize_address(csv_addresses))

    unique_in_webpage = list(webpage_addresses - csv_addresses)
    print sorted_nicely(unique_in_webpage)

if __name__ == "__main__":
    main()