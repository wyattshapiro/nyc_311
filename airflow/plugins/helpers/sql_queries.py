class SqlQueries:
    # DROP TABLES
    staging_service_request_table_drop = "DROP TABLE IF EXISTS staging_service_request;"
    staging_weather_table_drop = "DROP TABLE IF EXISTS staging_weather;"
    service_request_table_drop = "DROP TABLE IF EXISTS service_request;"
    weather_table_drop = "DROP TABLE IF EXISTS weather;"
    location_table_drop = "DROP TABLE IF EXISTS location;"
    complaint_type_table_drop = "DROP TABLE IF EXISTS complaint_type;"
    agency_table_drop = "DROP TABLE IF EXISTS agency;"
    submission_type_table_drop = "DROP TABLE IF EXISTS submission_type;"
    status_table_drop = "DROP TABLE IF EXISTS status;"

    # CREATE TABLES
    staging_service_request_table_create = ("""
    CREATE TABLE IF NOT EXISTS public.staging_service_request (
                                 unique_key varchar(256),
                                 created_date varchar(256),
                                 closed_date varchar(256),
                                 agency varchar(256),
                                 agency_name varchar(256),
                                 complaint_type varchar(256),
                                 descriptor varchar(256),
                                 incident_zip varchar(10),
                                 incident_address varchar(256),
                                 street_name varchar(256),
                                 address_type varchar(256),
                                 city varchar(256),
                                 facility_type varchar(256),
                                 status varchar(256),
                                 resolution_description varchar(1024),
                                 resolution_action_updated_date varchar(256),
                                 community_board varchar(256),
                                 bbl varchar(256),
                                 borough varchar(256),
                                 x_coordinate_state_plane int4,
                                 y_coordinate_state_plane int4,
                                 open_data_channel_type varchar(256),
                                 park_facility_name varchar(256),
                                 park_borough varchar(256),
                                 latitude float8,
                                 longitude float8,
                                 location varchar(256),
                                 location_address varchar(256),
                                 location_city varchar(256),
                                 location_state varchar(256),
                                 location_zip varchar(256),
                                 location_type varchar(256),
                                 cross_street_1 varchar(256),
                                 cross_street_2 varchar(256),
                                 intersection_street_1 varchar(256),
                                 intersection_street_2 varchar(256),
                                 landmark varchar(256)
                 );
    """)

    staging_weather_table_create = ("""
    CREATE TABLE IF NOT EXISTS public.staging_weather (
                                 time varchar(256),
                                 summary varchar(256),
                                 icon varchar(256),
                                 precip_intensity float4,
                                 precip_probability float4,
                                 precip_type varchar(256),
                                 temperature float4,
                                 apparent_temperature float4,
                                 dew_point float4,
                                 humidity float4,
                                 pressure float4,
                                 wind_speed float4,
                                 wind_gust float4,
                                 wind_bearing float4,
                                 cloud_cover float4,
                                 uv_index int4,
                                 visibility float4,
                                 ozone float4
                 );
    """)

    service_request_table_create = ("""
        CREATE TABLE IF NOT EXISTS public.service_request (
                                 service_request_id varchar(256) NOT NULL,
                                 created_date timestamp NOT NULL,
                                 closed_date timestamp NOT NULL,
                                 created_date_hour_id varchar(256) NOT NULL,
                                 agency_id varchar(256),
                                 complaint_type_id varchar(256),
                                 bbl_id varchar(10),
                                 status_id varchar(256),
                                 submission_type_id varchar(256),
                                 resolution_description varchar(1024),
                                 resolution_action_updated_date timestamp,
                                 CONSTRAINT service_request_pkey PRIMARY KEY (service_request_id)
                    );
    """)

    weather_table_create = ("""
    CREATE TABLE IF NOT EXISTS public.weather (
                                      date_hour_id varchar(256) NOT NULL,
                                      datetime timestamp NOT NULL,
                                      hour int NOT NULL,
                                      temperature float4 NOT NULL,
                                      apparent_temperature float4,
                                      summary varchar(256),
                                      humidity float4,
                                      precip_intensity float4,
                                      precip_probability float4,
                                      precip_type varchar(256),
                                      CONSTRAINT weather_pkey PRIMARY KEY (date_hour_id)
                 );
    """)

    location_table_create = ("""
    CREATE TABLE IF NOT EXISTS public.location (
                                bbl_id varchar(10) NOT NULL,
                                borough varchar(1),
                                block varchar(5),
                                lot varchar(4),
                                incident_address varchar(256),
                                city varchar(256),
                                incident_zip varchar(10),
                                latitude float8,
                                longitude float8,
                                CONSTRAINT location_pkey PRIMARY KEY (bbl_id)
                );
    """)

    complaint_type_table_create = ("""
        CREATE TABLE IF NOT EXISTS public.complaint_type (
                                       complaint_type_id INTEGER IDENTITY(0,1),
                                       complaint_type varchar(256),
                                       descriptor varchar(256),
                                       CONSTRAINT complaint_type_pkey PRIMARY KEY (complaint_type_id)
                                   );
    """)

    agency_table_create = ("""
        CREATE TABLE IF NOT EXISTS public.agency (
                                       agency_id INTEGER IDENTITY(0,1),
                                       agency_acronym varchar(10),
                                       agency_name varchar(256),
                                       CONSTRAINT agency_pkey PRIMARY KEY (agency_id)
                                   );
    """)

    submission_type_table_create = ("""
        CREATE TABLE IF NOT EXISTS public.submission_type (
                                       submission_type_id INTEGER IDENTITY(0,1),
                                       submission_type varchar(256),
                                       CONSTRAINT submission_type_pkey PRIMARY KEY (submission_type_id)
                                   );
    """)

    status_table_create = ("""
        CREATE TABLE IF NOT EXISTS public.status (
                                       status_id INTEGER IDENTITY(0,1),
                                       status varchar(256),
                                       CONSTRAINT status_pkey PRIMARY KEY (status_id)
                                   );
    """)

    # SELECT DATA FOR INSERT
    service_request_table_insert = ("""
        SELECT DISTINCT SR.unique_key,
                        cast(SR.created_date as timestamp),
                        cast(SR.closed_date as timestamp),
                        trunc(cast(SR.created_date as timestamp)) || '--' || extract(hour from cast(SR.created_date as timestamp)),
                        A.agency_id,
                        CT.complaint_type_id,
                        SR.bbl,
                        S.status_id,
                        ST.submission_type_id,
                        SR.resolution_description,
                        cast(SR.resolution_action_updated_date as timestamp)
        FROM staging_service_request SR
        JOIN agency A ON (SR.agency = A.agency_acronym AND SR.agency_name = A.agency_name)
        JOIN complaint_type CT ON (SR.complaint_type = CT.complaint_type AND SR.descriptor = CT.descriptor)
        JOIN status S ON (SR.status = S.status)
        JOIN submission_type ST ON (SR.open_data_channel_type = ST.submission_type)
        WHERE SR.status='Closed'
    """)

    weather_table_insert = ("""
        SELECT trunc(cast(time as timestamp)) || '--' || extract(hour from cast(time as timestamp)),
                cast(time as timestamp),
                extract(hour from cast(time as timestamp)) as hour,
                temperature,
                apparent_temperature,
                summary,
                humidity,
                precip_intensity,
                precip_probability,
                precip_type
        FROM staging_weather
    """)


    location_table_insert = ("""
        SELECT DISTINCT bbl,
                        substring(bbl,1,1) as borough,
                        substring(bbl,2,5) as block,
                        substring(bbl,7,4) as lot,
                        incident_address,
                        city,
                        incident_zip,
                        latitude,
                        longitude
        FROM staging_service_request
        WHERE bbl IS NOT NULL
    """)

    complaint_type_table_insert = ("""
        SELECT DISTINCT complaint_type, descriptor
        FROM staging_service_request
    """)

    agency_table_insert = ("""
        SELECT DISTINCT agency, agency_name
        FROM staging_service_request
    """)

    submission_type_table_insert = ("""
        SELECT DISTINCT open_data_channel_type
        FROM staging_service_request
    """)

    status_table_insert = ("""
        SELECT DISTINCT status
        FROM staging_service_request
    """)
