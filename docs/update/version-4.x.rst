Important information for :code:`pyfunceble >= 4.0.0`
-----------------------------------------------------

When you upgrade PyFunceble from :code:`<4.x` to any version :code:`4.x`
there will be:

- a SQL conversion if you use the :code:`--database-type` :code:`mysql`
  or :code:`mariadb`.
- a JSON to CSV conversion if one of those files is found in your filesystem:

   - :code:`inactive_db.json`
   - :code:`whois_db.json`

- The conversion of both SQL and json to CSV will take a "bit" of time as, it is
  done in a single process mode, to avoid any hick-ups instead of loading the entire
  file into memory. Loading the entire :code:`*.json` file into memory can have
  severe consequences depending on the size of the source file.

  .. note::

      Once the job is done the :code:`json2csv` shouldn't appear again for this or later
      :code:`4.x` releases.

- A workaround for waiting on the rather slow :code:`json2csv`, you can delete

   - :code:`inactive_db.json`
   - :code:`whois_db.json` (Very Very Very bad idea in the long run...)

  However you will probably not benefit for by deleting the :code:`whois_db.json`
  as this is the definitive slowest lookup process in the test flow, do to the
  limitation in available API call you can do to :code:`WHOIS` servers before
  getting banned. Therefore we **CAN NOT** recommend deleting this file, rather
  than waiting for the conversion to finish.

- The output directory structure have been altered to work with the ability to
  test more than one source at the time.
  Prior to version :code:`4.0.0.ax` the output hierarchy looked like
  :code:`output/domains/ACTIVE/list`.
  In Pyfunceble version :code:`>=4.x` this have been altered to include the source
  name and append to the folder structure.
  From this version it will therefor looks like
  :code:`output/{{ input_source_name }}/domains/ACTIVE list`.


.. note::

   As consequence of the time consuming conversion, we will advise you
   to run a simple pyfunceble command like:

   .. code-block:: console

      pyfunceble -d mypdns.org

      pyfunceble --database-type mariadb -d mypdns.org


How long time does it take
^^^^^^^^^^^^^^^^^^^^^^^^^^

A few numbers to help you schedule your upgrade process.

We have tested the SQL conversion with the following specifications

  - 2 Xeon CPU x86_64 (8 cores) 2 GHz
  - 48 GB ram.
  - 1 SSD Kingston KC-600
  - Mariadb 10.5, default config
  - Non dedicated

The database contains
  - Roughly :code:`265.000` records in the test tables
  - Approximately :code:`1.000.000` records within the :code:`pyfunceble_whois` table.

This process toke about 10 hours to complete.
