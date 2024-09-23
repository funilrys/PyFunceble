# `http_codes`

PyFunceble can interpret the status codes of a query into a "Human" readable
status. This is how you can configure PyFunceble for your own logic.

## Overview

```yaml title=".PyFunceble.overwrite.yaml"
http_codes:
  # Provides everything related to the HTTP code lookup interpolation.

  # Stops PyFunceble self management of the list.
  #
  # NOTE:
  #     This parameter is deprecated.
  self_managed: no

  list:
    # Dictionary with the status codes and their interpolation.

    up:
      # A list of status codes to consider as ACTIVE.
      - 100
      - 101
      - 102
      - 200
      - 201
      - 202
      - 203
      - 204
      - 205
      - 206
      - 207
      - 208
      - 226
      - 429
    potentially_down:
      # A list of status codes to consider as potentially INACTIVE.
      - 400
      - 402
      - 404
      - 409
      - 410
      - 412
      - 414
      - 415
      - 416
      - 451
    potentially_up:
      # A list of status codes to consider as potentially ACTIVE.
      - 000
      - 300
      - 301
      - 302
      - 303
      - 304
      - 305
      - 307
      - 308
      - 403
      - 405
      - 406
      - 407
      - 408
      - 411
      - 413
      - 417
      - 418
      - 421
      - 422
      - 423
      - 424
      - 426
      - 428
      - 431
      - 500
      - 501
      - 502
      - 503
      - 504
      - 505
      - 506
      - 507
      - 508
      - 510
      - 511
```
