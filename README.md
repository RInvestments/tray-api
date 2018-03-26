# Flask site for sun dance.

Currently we use flask to provide easy to use API of the database info, for other web applications.
The whole application is organized using flask-blueprints. I rely on OAuth (flask-dance) for
authentication. Currently using OAuth from github for authorizing data access. Also using https (secure)
for connection and mongodb with special user-role to access the data.


## How to run
Before you could run, you need to set bash environment variables.

- For mongodb access (URL+Password)

        ```
        export MONGO_URI=mongodb://<mongodb_username>:<mongodb_password>@<mongodb_server>/default_db?authSource=admin
        ```

- For github OAuth

        ```
        export GITHUB_CLIENT_ID=<your github Oauth client id>
        export GITHUB_CLIENT_SECRET=<your github Oauth secret>
        ```


```
python app.py
```

Ofcourse you can run this with nginx or gunicorn or any other webserver. But currently only using the
internal webserver.


## Webservice Info
`app.py` provides for main of the web based interface. Mongodb and other config is
in `config.py`. I have defined a package named `blue`. The subpackage `api` defines all the
routes blueprints. The subpackage `dbingress` defines all the classes which do the mongodb
queries. All the classes are derived from the base class `DBBase`.

There are 4 blueprints defined, each associated with a set of database queries. More will be
added in the future as per needs. To access any of the URLs you need to authenticate using OAuth from
github. To do that you need to create a github app and set the github info correctly. Put an issue, I can help
you set it up.

### ticker queries
These queries give information for an input ticker, for example description, employess count, etc.
Multiple tickers can be provided as ':' separated. Eg. '2333.HK:AMZN.NASDAQ:1301.TYO' etc.

- /tickerInfo/`ticker`/name
- /tickerInfo/`ticker`/industry
- /tickerInfo/`ticker`/sector
- /tickerInfo/`ticker`/description
- /tickerInfo/`ticker`/employeeCount
- /tickerInfo/`ticker`/streetAddress
- /tickerInfo/`ticker`/accountingCurrency/<year>


### accounting statement queries
These queries give information on accounting statements, viz. incomestatement (is), balance sheet (assets, liabs),
cash flow statement (cf_op, cf_inv, cf_fin). year can have value `all`, which will giveout data for all available years.
items can have value `all` which will giveout all available items in the statement. `/raw` gives string info.

- /accountingStatements/`ticker`/`statement`/`year`/`items`
- /accountingStatements/`ticker`/`statement`/`year`/`items`/raw


### industry info queries
These give out information on industry and sector. For example, it can give you industry list, sector list and tickers in a particular
(industry, sector) tuple. The url parameters viz, bourse, industry, sector can have value `all`.

- /industryInfo/`bourse`
- /industryInfo/`bourse`/`industry`
- /industryInfo/`bourse`/`industry`/`sector`


### quotes queries
These give info on daily quotes data. Currently quotes data is not available for Shenzen(SZ) and Shanghai(SH). It is available for
Hong Kong (HK), BSE, NSE, NASDAQ, NYSE, Tokyo (TYO). `Ticker` and `on_date` can have multiple values, ':' separated.  start_date
and end_date can only have single value. Date need to be in format YYYY-MM-DD.

- /tickerQuotesInfo/`ticker`/
- /tickerQuotesInfo/`ticker`/`start_date`/`end_date`
- /tickerQuotesInfo/`ticker`/`on_date`



## Author
Manohar Kuse <mpkuse@connect.ust.hk>
