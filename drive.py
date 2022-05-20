#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import crawling_melon

if __name__ == "__main__":
    if len(sys.argv) == 3:
        melon_items = crawling_melon.get_items_for_weekly(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        melon_items = crawling_melon.get_items_for_monthly(sys.argv[1])
    else:
        sys.exit(1)

    print(melon_items)
