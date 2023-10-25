from __future__ import annotations

from typing import List, TypedDict, Union


class ParamsItem(TypedDict):
    key: str
    value: str


class ServicetrackingparamsItem(TypedDict):
    service: str
    params: List[ParamsItem]


class Mainappwebresponsecontext(TypedDict):
    datasyncId: str
    loggedOut: bool
    trackingParam: str


class Webresponsecontextextensiondata(TypedDict):
    hasDecorated: bool


class Responsecontext(TypedDict):
    serviceTrackingParams: List[ServicetrackingparamsItem]
    maxAgeSeconds: int
    mainAppWebResponseContext: Mainappwebresponsecontext
    webResponseContextExtensionData: Webresponsecontextextensiondata


class Webcommandmetadata(TypedDict):
    url: str
    webPageType: str
    rootVe: int
    apiUrl: str


class Commandmetadata(TypedDict):
    webCommandMetadata: Webcommandmetadata


class Browseendpoint(TypedDict):
    browseId: str
    params: str
    canonicalBaseUrl: str


class Endpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata
    browseEndpoint: Browseendpoint


class Tabrenderer(TypedDict):
    endpoint: Endpoint
    title: str
    trackingParams: str


class TabsItem(TypedDict):
    tabRenderer: Tabrenderer


class ThumbnailsItem(TypedDict):
    url: str
    width: int
    height: int


class Thumbnail(TypedDict):
    thumbnails: List[ThumbnailsItem]


class RunsItem(TypedDict):
    text: str


class Videocounttext(TypedDict):
    runs: List[RunsItem]


class Accessibilitydata(TypedDict):
    label: str


class Accessibility(TypedDict):
    accessibilityData: Accessibilitydata


class Subscribercounttext(TypedDict):
    accessibility: Accessibility
    simpleText: str


class Browseendpoint0(TypedDict):
    browseId: str
    canonicalBaseUrl: str


class Navigationendpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata
    browseEndpoint: Browseendpoint0


class Title(TypedDict):
    simpleText: str


class Style(TypedDict):
    styleType: str


class Webcommandmetadata0(TypedDict):
    sendPost: bool
    apiUrl: str


class Commandmetadata0(TypedDict):
    webCommandMetadata: Webcommandmetadata0


class Subscribeendpoint(TypedDict):
    channelIds: List[str]
    params: str


class OnsubscribeendpointsItem(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    subscribeEndpoint: Subscribeendpoint


class Webcommandmetadata1(TypedDict):
    sendPost: bool


class Commandmetadata1(TypedDict):
    webCommandMetadata: Webcommandmetadata1


class Serviceendpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    unsubscribeEndpoint: Subscribeendpoint


class Buttonrenderer(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Videocounttext
    serviceEndpoint: Serviceendpoint
    accessibility: Accessibilitydata
    trackingParams: str


class Confirmbutton(TypedDict):
    buttonRenderer: Buttonrenderer


class Buttonrenderer0(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Videocounttext
    accessibility: Accessibilitydata
    trackingParams: str


class Cancelbutton(TypedDict):
    buttonRenderer: Buttonrenderer0


class Confirmdialogrenderer(TypedDict):
    trackingParams: str
    dialogMessages: List[Videocounttext]
    confirmButton: Confirmbutton
    cancelButton: Cancelbutton
    primaryIsCancel: bool


class Popup(TypedDict):
    confirmDialogRenderer: Confirmdialogrenderer


class Openpopupaction(TypedDict):
    popup: Popup
    popupType: str


class ActionsItem(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction


class Signalserviceendpoint(TypedDict):
    signal: str
    actions: List[ActionsItem]


class OnunsubscribeendpointsItem(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    signalServiceEndpoint: Signalserviceendpoint


class Subscribebuttonrenderer(TypedDict):
    buttonText: Videocounttext
    subscribed: bool
    enabled: bool
    type: str
    channelId: str
    showPreferences: bool
    subscribedButtonText: Videocounttext
    unsubscribedButtonText: Videocounttext
    trackingParams: str
    unsubscribeButtonText: Videocounttext
    style: Style
    subscribeAccessibility: Accessibility
    unsubscribeAccessibility: Accessibility
    subscribedEntityKey: str
    onSubscribeEndpoints: List[OnsubscribeendpointsItem]
    onUnsubscribeEndpoints: List[OnunsubscribeendpointsItem]


class Subscribebutton(TypedDict):
    subscribeButtonRenderer: Subscribebuttonrenderer


class Icon(TypedDict):
    iconType: str


class Metadatabadgerenderer(TypedDict):
    icon: Icon
    style: str
    tooltip: str
    trackingParams: str
    accessibilityData: Accessibilitydata


class OwnerbadgesItem(TypedDict):
    metadataBadgeRenderer: Metadatabadgerenderer


class Gridchannelrenderer(TypedDict):
    channelId: str
    thumbnail: Thumbnail
    videoCountText: Videocounttext
    subscriberCountText: Subscribercounttext
    navigationEndpoint: Navigationendpoint
    title: Title
    subscribeButton: Subscribebutton
    ownerBadges: List[OwnerbadgesItem]
    trackingParams: str


class ItemsItem(TypedDict):
    gridChannelRenderer: Gridchannelrenderer


class Gridchannelrenderer0(TypedDict):
    channelId: str
    thumbnail: Thumbnail
    videoCountText: Videocounttext
    subscriberCountText: Subscribercounttext
    navigationEndpoint: Navigationendpoint
    title: Title
    subscribeButton: Subscribebutton
    trackingParams: str


class ItemsItem0(TypedDict):
    gridChannelRenderer: Gridchannelrenderer0


class Gridrenderer(TypedDict):
    items: List[Union[ItemsItem, ItemsItem0]]
    trackingParams: str
    targetId: str


class ContentsItem(TypedDict):
    gridRenderer: Gridrenderer


class Itemsectionrenderer(TypedDict):
    contents: List[ContentsItem]
    trackingParams: str


class ContentsItem0(TypedDict):
    itemSectionRenderer: Itemsectionrenderer


class ContenttypesubmenuitemsItem(TypedDict):
    endpoint: Endpoint
    title: str
    selected: bool


class Channelsubmenurenderer(TypedDict):
    contentTypeSubMenuItems: List[ContenttypesubmenuitemsItem]


class Submenu(TypedDict):
    channelSubMenuRenderer: Channelsubmenurenderer


class Sectionlistrenderer(TypedDict):
    contents: List[ContentsItem0]
    trackingParams: str
    subMenu: Submenu
    targetId: str
    disablePullToRefresh: bool


class Content(TypedDict):
    sectionListRenderer: Sectionlistrenderer


class Tabrenderer0(TypedDict):
    endpoint: Endpoint
    title: str
    selected: bool
    content: Content
    trackingParams: str


class TabsItem0(TypedDict):
    tabRenderer: Tabrenderer0


class TabsItem1(TypedDict):
    expandableTabRenderer: ContenttypesubmenuitemsItem


class Twocolumnbrowseresultsrenderer(TypedDict):
    tabs: List[Union[TabsItem1, TabsItem0, TabsItem]]


class Contents(TypedDict):
    twoColumnBrowseResultsRenderer: Twocolumnbrowseresultsrenderer


class Webcommandmetadata2(TypedDict):
    url: str
    webPageType: str
    rootVe: int


class Commandmetadata2(TypedDict):
    webCommandMetadata: Webcommandmetadata2


class Urlendpoint(TypedDict):
    url: str
    target: str


class Innertubecommand(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    urlEndpoint: Urlendpoint


class Ontap(TypedDict):
    innertubeCommand: Innertubecommand


class CommandrunsItem(TypedDict):
    startIndex: int
    length: int
    onTap: Ontap


class Firstlink(TypedDict):
    content: str
    commandRuns: List[CommandrunsItem]


class Ontap0(TypedDict):
    innertubeCommand: Endpoint


class CommandrunsItem0(TypedDict):
    startIndex: int
    length: int
    onTap: Ontap0


class More(TypedDict):
    content: str
    commandRuns: List[CommandrunsItem0]


class Channelheaderlinksviewmodel(TypedDict):
    firstLink: Firstlink
    more: More


class Headerlinks(TypedDict):
    channelHeaderLinksViewModel: Channelheaderlinksviewmodel


class Buttonrenderer1(TypedDict):
    style: str
    size: str
    isDisabled: bool
    icon: Icon
    accessibility: Accessibilitydata
    trackingParams: str
    accessibilityData: Accessibility


class State(TypedDict):
    buttonRenderer: Buttonrenderer1


class StatesItem(TypedDict):
    stateId: int
    nextStateId: int
    state: State


class Modifychannelnotificationpreferenceendpoint(TypedDict):
    params: str


class Serviceendpoint0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    modifyChannelNotificationPreferenceEndpoint: Modifychannelnotificationpreferenceendpoint


class Menuserviceitemrenderer(TypedDict):
    text: Title
    icon: Icon
    serviceEndpoint: Serviceendpoint0
    trackingParams: str
    isSelected: bool


class ItemsItem1(TypedDict):
    menuServiceItemRenderer: Menuserviceitemrenderer


class Menuserviceitemrenderer0(TypedDict):
    text: Videocounttext
    icon: Icon
    serviceEndpoint: OnunsubscribeendpointsItem
    trackingParams: str


class ItemsItem2(TypedDict):
    menuServiceItemRenderer: Menuserviceitemrenderer0


class Menupopuprenderer(TypedDict):
    items: List[Union[ItemsItem2, ItemsItem1]]


class Popup0(TypedDict):
    menuPopupRenderer: Menupopuprenderer


class Openpopupaction0(TypedDict):
    popup: Popup0
    popupType: str


class CommandsItem(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction0


class Commandexecutorcommand(TypedDict):
    commands: List[CommandsItem]


class Command(TypedDict):
    clickTrackingParams: str
    commandExecutorCommand: Commandexecutorcommand


class Subscriptionnotificationtogglebuttonrenderer(TypedDict):
    states: List[StatesItem]
    currentStateId: int
    trackingParams: str
    command: Command
    targetId: str
    secondaryIcon: Icon


class Notificationpreferencebutton(TypedDict):
    subscriptionNotificationToggleButtonRenderer: Subscriptionnotificationtogglebuttonrenderer


class Subscribebuttonrenderer0(TypedDict):
    buttonText: Videocounttext
    subscribed: bool
    enabled: bool
    type: str
    channelId: str
    showPreferences: bool
    subscribedButtonText: Videocounttext
    unsubscribedButtonText: Videocounttext
    trackingParams: str
    unsubscribeButtonText: Videocounttext
    subscribeAccessibility: Accessibility
    unsubscribeAccessibility: Accessibility
    notificationPreferenceButton: Notificationpreferencebutton
    subscribedEntityKey: str
    onSubscribeEndpoints: List[OnsubscribeendpointsItem]
    onUnsubscribeEndpoints: List[OnunsubscribeendpointsItem]


class Subscribebutton0(TypedDict):
    subscribeButtonRenderer: Subscribebuttonrenderer0


class Visittracking(TypedDict):
    remarketingPing: str


class Serviceendpoint1(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    ypcGetOffersEndpoint: Modifychannelnotificationpreferenceendpoint


class Buttonrenderer2(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Videocounttext
    serviceEndpoint: Serviceendpoint1
    trackingParams: str
    accessibilityData: Accessibility
    targetId: str


class Sponsorbutton(TypedDict):
    buttonRenderer: Buttonrenderer2


class Channeltaglinerenderer(TypedDict):
    content: str
    maxLines: int
    moreLabel: str
    moreEndpoint: Endpoint
    moreIcon: Icon


class Tagline(TypedDict):
    channelTaglineRenderer: Channeltaglinerenderer


class C4tabbedheaderrenderer(TypedDict):
    channelId: str
    title: str
    navigationEndpoint: Navigationendpoint
    avatar: Thumbnail
    banner: Thumbnail
    badges: List[OwnerbadgesItem]
    headerLinks: Headerlinks
    subscribeButton: Subscribebutton0
    visitTracking: Visittracking
    subscriberCountText: Subscribercounttext
    tvBanner: Thumbnail
    mobileBanner: Thumbnail
    trackingParams: str
    sponsorButton: Sponsorbutton
    channelHandleText: Videocounttext
    style: str
    videosCountText: Videocounttext
    tagline: Tagline


class Header(TypedDict):
    c4TabbedHeaderRenderer: C4tabbedheaderrenderer


class Channelmetadatarenderer(TypedDict):
    title: str
    description: str
    rssUrl: str
    channelConversionUrl: str
    externalId: str
    keywords: str
    ownerUrls: List[str]
    avatar: Thumbnail
    channelUrl: str
    isFamilySafe: bool
    availableCountryCodes: List[str]
    androidDeepLink: str
    androidAppindexingLink: str
    iosAppindexingLink: str
    vanityChannelUrl: str


class Metadata(TypedDict):
    channelMetadataRenderer: Channelmetadatarenderer


class Browseendpoint1(TypedDict):
    browseId: str


class Endpoint0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata
    browseEndpoint: Browseendpoint1


class Topbarlogorenderer(TypedDict):
    iconImage: Icon
    tooltipText: Videocounttext
    endpoint: Endpoint0
    trackingParams: str
    overrideEntityKey: str


class Logo(TypedDict):
    topbarLogoRenderer: Topbarlogorenderer


class Websearchboxconfig(TypedDict):
    requestLanguage: str
    requestDomain: str
    hasOnscreenKeyboard: bool
    focusSearchbox: bool


class Config(TypedDict):
    webSearchboxConfig: Websearchboxconfig


class Searchendpoint(TypedDict):
    query: str


class Searchendpoint0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    searchEndpoint: Searchendpoint


class Buttonrenderer3(TypedDict):
    style: str
    size: str
    isDisabled: bool
    icon: Icon
    trackingParams: str
    accessibilityData: Accessibility


class Clearbutton(TypedDict):
    buttonRenderer: Buttonrenderer3


class Fusionsearchboxrenderer(TypedDict):
    icon: Icon
    placeholderText: Videocounttext
    config: Config
    trackingParams: str
    searchEndpoint: Searchendpoint0
    clearButton: Clearbutton


class Searchbox(TypedDict):
    fusionSearchboxRenderer: Fusionsearchboxrenderer


class Uploadendpoint(TypedDict):
    hack: bool


class Navigationendpoint0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    uploadEndpoint: Uploadendpoint


class Compactlinkrenderer(TypedDict):
    icon: Icon
    title: Videocounttext
    navigationEndpoint: Navigationendpoint0
    trackingParams: str
    style: str


class ItemsItem3(TypedDict):
    compactLinkRenderer: Compactlinkrenderer


class Signalnavigationendpoint(TypedDict):
    signal: str


class Navigationendpoint1(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata2
    signalNavigationEndpoint: Signalnavigationendpoint


class Compactlinkrenderer0(TypedDict):
    icon: Icon
    title: Videocounttext
    navigationEndpoint: Navigationendpoint1
    trackingParams: str
    style: str


class ItemsItem4(TypedDict):
    compactLinkRenderer: Compactlinkrenderer0


class Browseendpoint2(TypedDict):
    browseId: str
    params: str


class Navigationendpoint2(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata
    browseEndpoint: Browseendpoint2


class Compactlinkrenderer1(TypedDict):
    icon: Icon
    title: Videocounttext
    navigationEndpoint: Navigationendpoint2
    trackingParams: str
    style: str


class ItemsItem5(TypedDict):
    compactLinkRenderer: Compactlinkrenderer1


class Multipagemenusectionrenderer(TypedDict):
    items: List[Union[ItemsItem4, ItemsItem5, ItemsItem3]]
    trackingParams: str


class SectionsItem(TypedDict):
    multiPageMenuSectionRenderer: Multipagemenusectionrenderer


class Multipagemenurenderer(TypedDict):
    sections: List[SectionsItem]
    trackingParams: str
    style: str


class Menurenderer(TypedDict):
    multiPageMenuRenderer: Multipagemenurenderer


class Topbarmenubuttonrenderer(TypedDict):
    icon: Icon
    menuRenderer: Menurenderer
    trackingParams: str
    accessibility: Accessibility
    tooltip: str
    style: str


class TopbarbuttonsItem(TypedDict):
    topbarMenuButtonRenderer: Topbarmenubuttonrenderer


class Multipagemenurenderer0(TypedDict):
    trackingParams: str
    style: str
    showLoadingSpinner: bool


class Popup1(TypedDict):
    multiPageMenuRenderer: Multipagemenurenderer0


class Openpopupaction1(TypedDict):
    popup: Popup1
    popupType: str
    beReused: bool


class ActionsItem0(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction1


class Signalserviceendpoint0(TypedDict):
    signal: str
    actions: List[ActionsItem0]


class Menurequest(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalserviceendpoint0


class Updateunseencountendpoint(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata0
    signalServiceEndpoint: Signalnavigationendpoint


class Notificationtopbarbuttonrenderer(TypedDict):
    icon: Icon
    menuRequest: Menurequest
    style: str
    trackingParams: str
    accessibility: Accessibility
    tooltip: str
    updateUnseenCountEndpoint: Updateunseencountendpoint
    notificationCount: int
    handlerDatas: List[str]


class TopbarbuttonsItem0(TypedDict):
    notificationTopbarButtonRenderer: Notificationtopbarbuttonrenderer


class Avatar(TypedDict):
    thumbnails: List[ThumbnailsItem]
    accessibility: Accessibility


class Topbarmenubuttonrenderer0(TypedDict):
    avatar: Avatar
    menuRequest: Menurequest
    trackingParams: str
    accessibility: Accessibility
    tooltip: str


class TopbarbuttonsItem1(TypedDict):
    topbarMenuButtonRenderer: Topbarmenubuttonrenderer0


class Hotkeydialogsectionoptionrenderer(TypedDict):
    label: Videocounttext
    hotkey: str


class OptionsItem(TypedDict):
    hotkeyDialogSectionOptionRenderer: Hotkeydialogsectionoptionrenderer


class Hotkeydialogsectionoptionrenderer0(TypedDict):
    label: Videocounttext
    hotkey: str
    hotkeyAccessibilityLabel: Accessibility


class OptionsItem0(TypedDict):
    hotkeyDialogSectionOptionRenderer: Hotkeydialogsectionoptionrenderer0


class Hotkeydialogsectionrenderer(TypedDict):
    title: Videocounttext
    options: List[Union[OptionsItem, OptionsItem0]]


class SectionsItem0(TypedDict):
    hotkeyDialogSectionRenderer: Hotkeydialogsectionrenderer


class Hotkeydialogsectionrenderer0(TypedDict):
    title: Videocounttext
    options: List[OptionsItem]


class SectionsItem1(TypedDict):
    hotkeyDialogSectionRenderer: Hotkeydialogsectionrenderer0


class Buttonrenderer4(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Videocounttext
    trackingParams: str


class Dismissbutton(TypedDict):
    buttonRenderer: Buttonrenderer4


class Hotkeydialogrenderer(TypedDict):
    title: Videocounttext
    sections: List[Union[SectionsItem0, SectionsItem1]]
    dismissButton: Dismissbutton
    trackingParams: str


class Hotkeydialog(TypedDict):
    hotkeyDialogRenderer: Hotkeydialogrenderer


class ActionsItem1(TypedDict):
    clickTrackingParams: str
    signalAction: Signalnavigationendpoint


class Signalserviceendpoint1(TypedDict):
    signal: str
    actions: List[ActionsItem1]


class Command0(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    signalServiceEndpoint: Signalserviceendpoint1


class Buttonrenderer5(TypedDict):
    trackingParams: str
    command: Command0


class Backbutton(TypedDict):
    buttonRenderer: Buttonrenderer5


class Buttonrenderer6(TypedDict):
    style: str
    size: str
    isDisabled: bool
    text: Videocounttext
    trackingParams: str
    command: Command0


class A11yskipnavigationbutton(TypedDict):
    buttonRenderer: Buttonrenderer6


class Voicesearchdialogrenderer(TypedDict):
    placeholderHeader: Videocounttext
    promptHeader: Videocounttext
    exampleQuery1: Videocounttext
    exampleQuery2: Videocounttext
    promptMicrophoneLabel: Videocounttext
    loadingHeader: Videocounttext
    connectionErrorHeader: Videocounttext
    connectionErrorMicrophoneLabel: Videocounttext
    permissionsHeader: Videocounttext
    permissionsSubtext: Videocounttext
    disabledHeader: Videocounttext
    disabledSubtext: Videocounttext
    microphoneButtonAriaLabel: Videocounttext
    exitButton: Clearbutton
    trackingParams: str
    microphoneOffPromptHeader: Videocounttext


class Popup2(TypedDict):
    voiceSearchDialogRenderer: Voicesearchdialogrenderer


class Openpopupaction2(TypedDict):
    popup: Popup2
    popupType: str


class ActionsItem2(TypedDict):
    clickTrackingParams: str
    openPopupAction: Openpopupaction2


class Signalserviceendpoint2(TypedDict):
    signal: str
    actions: List[ActionsItem2]


class Serviceendpoint2(TypedDict):
    clickTrackingParams: str
    commandMetadata: Commandmetadata1
    signalServiceEndpoint: Signalserviceendpoint2


class Buttonrenderer7(TypedDict):
    style: str
    size: str
    isDisabled: bool
    serviceEndpoint: Serviceendpoint2
    icon: Icon
    tooltip: str
    trackingParams: str
    accessibilityData: Accessibility


class Voicesearchbutton(TypedDict):
    buttonRenderer: Buttonrenderer7


class Desktoptopbarrenderer(TypedDict):
    logo: Logo
    searchbox: Searchbox
    trackingParams: str
    countryCode: str
    topbarButtons: List[
        Union[TopbarbuttonsItem0, TopbarbuttonsItem, TopbarbuttonsItem1]
    ]
    hotkeyDialog: Hotkeydialog
    backButton: Backbutton
    forwardButton: Backbutton
    a11ySkipNavigationButton: A11yskipnavigationbutton
    voiceSearchButton: Voicesearchbutton


class Topbar(TypedDict):
    desktopTopbarRenderer: Desktoptopbarrenderer


class LinkalternatesItem(TypedDict):
    hrefUrl: str


class Microformatdatarenderer(TypedDict):
    urlCanonical: str
    title: str
    description: str
    thumbnail: Thumbnail
    siteName: str
    appName: str
    androidPackage: str
    iosAppStoreId: str
    iosAppArguments: str
    ogType: str
    urlApplinksWeb: str
    urlApplinksIos: str
    urlApplinksAndroid: str
    urlTwitterIos: str
    urlTwitterAndroid: str
    twitterCardType: str
    twitterSiteHandle: str
    schemaDotOrgType: str
    noindex: bool
    unlisted: bool
    familySafe: bool
    tags: List[str]
    availableCountries: List[str]
    linkAlternates: List[LinkalternatesItem]


class Microformat(TypedDict):
    microformatDataRenderer: Microformatdatarenderer


class Resetchannelunreadcountcommand(TypedDict):
    channelId: str


class OnresponsereceivedactionsItem(TypedDict):
    clickTrackingParams: str
    resetChannelUnreadCountCommand: Resetchannelunreadcountcommand


class Subscriptionstateentity(TypedDict):
    key: str
    subscribed: bool


class Payload(TypedDict):
    subscriptionStateEntity: Subscriptionstateentity


class MutationsItem(TypedDict):
    entityKey: str
    type: str
    payload: Payload


class Timestamp(TypedDict):
    seconds: str
    nanos: int


class Entitybatchupdate(TypedDict):
    mutations: List[MutationsItem]
    timestamp: Timestamp


class Frameworkupdates(TypedDict):
    entityBatchUpdate: Entitybatchupdate


class Root(TypedDict):
    responseContext: Responsecontext
    contents: Contents
    header: Header
    metadata: Metadata
    trackingParams: str
    topbar: Topbar
    microformat: Microformat
    onResponseReceivedActions: List[OnresponsereceivedactionsItem]
    frameworkUpdates: Frameworkupdates
