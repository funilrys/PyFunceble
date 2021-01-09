Important information for :code:`>= 3.2.11`
-----------------------------------------------

When you update from dev@<=3.2.10 or master@<=3.2.2 to newer release, there
will be made a SQL conversion of the databases table layout.
This can take up a sagnificent amount of time based on the size of the
database.

The table layout converion is being made to:

1. Minimize the total size

2. Optimize the sql flow and minimizing the read/write to save disk I/O.

3. Minimize the number of SQL queries being made

It have been seen taking days to convert these tables on very large
installations.
