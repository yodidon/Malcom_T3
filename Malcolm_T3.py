
#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# jordigarnacho
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog

SITE_IDENTIFIER = 'Malcolm_T3'
SITE_NAME = 'Malcolm_T3'
SITE_DESC = 'Malcolm in the midle, streaming, séries'

URL_MAIN = 'http://malcolm-streaming.com/'

#FUNCTION_SEARCH = 'showMovies'

SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_SERIES = (URL_MAIN, 'showMovies')
SERIE_SERIES2 = (URL_MAIN, 'showMovies')
#SERIE_GENRES = (True, 'showGenres')

#loader function
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Malcolm in the midle ()', 'news.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['News', URL_MAIN + 'saison-7/episode-17/une-dent-contre-toi'] )
    

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
def showMoviesOLD(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<\/i> <a class="a-panel-head-gauche" href="([^"]+)">([^<>]+)<\/a>.+?<img SRC="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    VSlog(aResult)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl    = aEntry[0]
            sTitle  = aEntry[1]
            sThumb = aEntry[2]
            sThumb = URL_MAIN + sThumb
            

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            #oOutputParameterHandler.addParameter('referer', sUrl) # URL d'origine, parfois utile comme référence
            oGui.addMovie(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

#search the next page
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'En cours'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    

    sPattern = 'list-group-item.+?href=.+?\/i> (\w+).(\d)<\/a'

    
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #VSlog(aResult)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl    = URL_MAIN + 'saison'+'-' + aEntry[1]
            sTitle  = 'Saison' + aEntry[1]
            sThumb =''
            #sThumb = aEntry[2]
            #sThumb = URL_MAIN + sThumb
            

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            #oOutputParameterHandler.addParameter('referer', sUrl) # URL d'origine, parfois utile comme référence
            oGui.addMovie(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

#search the next page
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'En cours'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

#search hosts
def showHosters(): #recherche et affiche les hotes

    UrlEpisode = URL_MAIN + sUrl  + 'mystream'
    referer= UrlEpisode
    
    
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de parametre
    sUrl = oInputParameterHandler.getValue('siteUrl') #apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #appelle le titre
    sThumb = oInputParameterHandler.getValue('sThumb') #appelle le poster
    referer = oInputParameterHandler.getValue('referer') # récupere l'URL appelante
    
    oRequestHandler = cRequestHandler(sUrl) # requete sur l'url
    oRequestHandler.addHeaderEntry('Referer', referer) # parametre pour passer l'URL appelante (n'est pas forcement necessaire)
    sHtmlContent = oRequestHandler.request() # requete sur l'url

    oParser = cParser()
    sPattern = '<iframe.+?src="([^"]+)"'
    #ici nous cherchons toute les sources iframe

    aResult = oParser.parse(sHtmlContent, sPattern)
    #pensez a faire un VSlog(str(aResult)) pour verifier

    # si un lien ne s'affiche pas, peut etre que l'hote n'est pas supporte par l'addon
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl) #recherche l'hote dans l'addon
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle) #nom affiche
                oHoster.setFileName(sMovieTitle) #idem
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                #affiche le lien (oGui, oHoster, url du lien, poster)

    oGui.setEndOfDirectory() #fin

# Pour les series, il y a generalement une etape en plus pour la selection des episodes ou saisons.
def ShowSerieSaisonEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    #VSlog('je suis la')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<\/i> <a class="a-panel-head-gauche" href="([^"]+)">([^<>]+)<\/a>.+?<img SRC="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl    = URL_MAIN + aEntry[0]
            sTitle  = aEntry[1]
            sThumb = aEntry[2]
            sThumb = URL_MAIN + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()