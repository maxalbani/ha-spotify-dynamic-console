#######################################################
# CREA IL SENSORE DELLA CONSOLE CON RELATIVI ATTRIBUTI 
# E POPOLA LA LISTA DEI GENERI E DEI MEDIA_PLAYER 
#######################################################

entitySource = data.get('entity_source')
entityGenre = data.get('entity_genre')
if entitySource is None or entityGenre is None:
    logger.warning("===== I parametri entity_source e entity_genre sono richiesti.")
    service_data = {'title': 'Spotify Console - spotify_init','message':'I parametri entity_source e entity_genre sono richiesti'}
    hass.services.call('persistent_notification', 'create', service_data, False)    
else:

    sensor_name = 'sensor.spotify_console'
    sensor_state = 'on'
    attributes = {
      'playlists' : 
        [
          'Focus#Massima Concentrazione#spotify:playlist:37i9dQZF1DXbA4Uw2yEsP9',    
          'Focus#Lavorare con la musica#spotify:playlist:37i9dQZF1DXcb7YJnr6Ck4',
          'Relax#A Fine Giornata#spotify:playlist:37i9dQZF1DWUeDwH47meQn',
          'Relax#No Stress#spotify:playlist:37i9dQZF1DXc0aozDLZsk7',
          'Hits#Hot Hits Italia#spotify:playlist:37i9dQZF1DX6wfQutivYYr',
          'Hits#Today Top Hits#spotify:playlist:37i9dQZF1DXcBWIGoYBM5M',
          'Country#Forever Country#spotify:playlist:37i9dQZF1DX9hWdQ46pHPo',
          'Country#Hot Country#spotify:playlist:37i9dQZF1DX1lVhptIYRda',
          'Rock#Rock Classics#spotify:playlist:37i9dQZF1DWXRqgorJj26U',
          'Rock#Rock Ballads#spotify:playlist:37i9dQZF1DWXs1L3AC0Xio'
        ],
       'sources' :
        [
            'Sala#Echo Sala',
            'Studio#Echo Studio',
            'Bagno#Echo Bagno',
            'Camera#Echo Camera'
        ]
    }

    hass.states.set(sensor_name, sensor_state, attributes)
    
    # LOAD INPUT SELECT GENRES
    
    playlists = hass.states.get('sensor.spotify_console').attributes['playlists']
    
    generi = []
    generi_unique = ['Seleziona Genere']
    
    for playlist in playlists:
        objPlaylist = playlist.split("#")
        generi.append(objPlaylist[0])
    else:
        for i in generi: 
            if i not in generi_unique: 
                generi_unique.append(i)    
        else:
            service_data = {'entity_id': entityGenre, 
                            'options': generi_unique }
            hass.services.call('input_select', 'set_options', service_data, False)

    # LOAD INPUT SELECT SOURCES
    
    sources = hass.states.get('sensor.spotify_console').attributes['sources']
    
    array_sources = ['Seleziona Speaker']
    
    for source in sources:
        objSource = source.split("#")
        array_sources.append(objSource[0])
    else:
        service_data = {'entity_id': entitySource, 
                        'options': array_sources }
        hass.services.call('input_select', 'set_options', service_data, False)