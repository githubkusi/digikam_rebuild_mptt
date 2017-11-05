# Rebuild the tree traversal data of a MySQL db in digikam

This script rebuilds the columns Tags.lft and Tags.rgt from scratch, which are used to search for tags in digikam. 

Digikam up to at least v5.6 in conjunction with a MySQL db has issues when moving tags in the tag hierarchy. As a result, the search functionality for tags returns unexpected results. This script fixes an already broken database by recreating the columns Tags.lft and Tags.rgt from Tags.id and Tags.pid

Digikam uses a Modified Preorder Tree Traversal algorithm for fast hierarchical tags queries. Here's a description how it works: https://www.sitepoint.com/hierarchical-data-database-2/

## Prerequisites (OpenSuse)

```
zypper install python3-networkx python3-devel
pip install mysqlclient
```

## Usage
```
./rebuild-mptt.py --user <db username> --password <db passwd> --database <core db name>
```

## Warning
This is a very simple tool, no error checking nor sanity checks. Make sure you backup your database before using this tool



