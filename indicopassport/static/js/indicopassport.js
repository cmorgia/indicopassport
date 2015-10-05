ndRegForm.config(function($provide){
    $provide.decorator('ndSectionDirective',function($delegate){
        var directive = $delegate[0];
        var compile = directive.compile;
        directive.compile = function(tElement,tAttrs) {
            var link = compile.apply(this,arguments);
            var base = Indico.Urls.Base;
            var jarsBase = "/indico/static/assets/plugins/indicopassport/jars/";
            var appletJar = jarsBase+"swipeapplet.jar";
            var readerJar = jarsBase+"mmmreader.jar";
            var archive = appletJar+","+readerJar;
            return function(scope,elem,attrs) {
                var name = scope.section.directives;
                if (name=="nd-passport-section") {
                    elem.append("<applet name=\"MyApplet\" code=swipeapplet.SwipeApplet.class " +
                        "codebase=\""+jarsBase+"\" archive=\"swipeapplet.jar,mmmreader.jar\"  style=\"width: 400px; height: 50px\">" +
                        "Browser Does not support Java </applet>");
                }
                link.apply(this,arguments);
                //Extend link here if needed
            };
        };

        return $delegate;
    });
});

$.fn.xpathEvaluate = function (xpathExpression) {
    // NOTE: vars not declared local for debug purposes
    $this = this.first(); // Don't make me deal with multiples before coffee

    // Evaluate xpath and retrieve matching nodes
    xpathResult = this[0].evaluate(xpathExpression, this[0], null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);

    result = [];
    while (elem = xpathResult.iterateNext()) {
        result.push(elem);
    }

    $result = jQuery([]).pushStack( result );
    return $result;
};

function findElement(caption) {
    var selector = "//label[text()=\""+caption+"\"]/ancestor::tr/td[2]//ng-form/*[1]";
    var element = $(document).xpathEvaluate(selector);
    return element;
}

function readerdata(controlId) {
    var mapOfFields = {
        "First Name":"GetGivenName",
        "Last Name":"GetSurname",
        "Birth Date":"GetDateOfBirth",
        "Passport ID":"GetDocumentNumber",
        "Passport Expire":"GetDateOfExpiry",
        "Passport Origin":"GetIssuer"
    };
    if (controlId == "ocr") {
        for (var key in mapOfFields) {
            var element = findElement(key);
            var methodName = mapOfFields[key];
            var value = MyApplet[methodName]();
            if (key=="Passport Origin") {
                value = countryMap[value];
            } else if (key=="Passport Expire") {
                value = "20"+value;
            } else if (key=="Birth Date") {
                value = "20"+value;
            }

            element.val(value);
        }
    } else {
        console.log("Unsupported scanning method");
    }
}

var countryMap = {
    'DZA': 'DZ',
    'AGO': 'AO',
    'EGY': 'EG',
    'BGD': 'BD',
    'NER': 'NE',
    'LIE': 'LI',
    'NAM': 'NA',
    'BGR': 'BG',
    'BOL': 'BO',
    'GHA': 'GH',
    'CCK': 'CC',
    'PAK': 'PK',
    'CPV': 'CV',
    'JOR': 'JO',
    'LBR': 'LR',
    'LBY': 'LY',
    'MYS': 'MY',
    'IOT': 'IO',
    'PRI': 'PR',
    'MYT': 'YT',
    'PRK': 'KP',
    'PSE': 'PS',
    'TZA': 'TZ',
    'BWA': 'BW',
    'KHM': 'KH',
    'UMI': 'UM',
    'TTO': 'TT',
    'PRY': 'PY',
    'HKG': 'HK',
    'SAU': 'SA',
    'LBN': 'LB',
    'SVN': 'SI',
    'BFA': 'BF',
    'SVK': 'SK',
    'MRT': 'MR',
    'HRV': 'HR',
    'CHL': 'CL',
    'CHN': 'CN',
    'KNA': 'KN',
    'JAM': 'JM',
    'SMR': 'SM',
    'GIB': 'GI',
    'DJI': 'DJ',
    'GIN': 'GN',
    'FIN': 'FI',
    'URY': 'UY',
    'VAT': 'VA',
    'STP': 'ST',
    'SYC': 'SC',
    'NPL': 'NP',
    'CXR': 'CX',
    'LAO': 'LA',
    'YEM': 'YE',
    'BVT': 'BV',
    'ZAF': 'ZA',
    'KIR': 'KI',
    'PHL': 'PH',
    'SXM': 'SX',
    'ROU': 'RO',
    'VIR': 'VI',
    'SYR': 'SY',
    'MAC': 'MO',
    'NIC': 'NI',
    'MLT': 'MT',
    'KAZ': 'KZ',
    'TCA': 'TC',
    'PYF': 'PF',
    'NIU': 'NU',
    'DMA': 'DM',
    'GBR': 'GB',
    'BEN': 'BJ',
    'GUF': 'GF',
    'BEL': 'BE',
    'MSR': 'MS',
    'TGO': 'TG',
    'DEU': 'DE',
    'GUM': 'GU',
    'LKA': 'LK',
    'SSD': 'SS',
    'FLK': 'FK',
    'PCN': 'PN',
    'BES': 'BQ',
    'GUY': 'GY',
    'CRI': 'CR',
    'COK': 'CK',
    'MAR': 'MA',
    'MNP': 'MP',
    'LSO': 'LS',
    'HUN': 'HU',
    'TKM': 'TM',
    'SUR': 'SR',
    'NLD': 'NL',
    'BMU': 'BM',
    'HMD': 'HM',
    'TCD': 'TD',
    'GEO': 'GE',
    'MNE': 'ME',
    'MNG': 'MN',
    'MHL': 'MH',
    'MTQ': 'MQ',
    'BLZ': 'BZ',
    'NFK': 'NF',
    'MMR': 'MM',
    'AFG': 'AF',
    'BDI': 'BI',
    'VGB': 'VG',
    'BLR': 'BY',
    'BLM': 'BL',
    'GRD': 'GD',
    'TKL': 'TK',
    'GRC': 'GR',
    'GRL': 'GL',
    'SHN': 'SH',
    'AND': 'AD',
    'MOZ': 'MZ',
    'TJK': 'TJ',
    'THA': 'TH',
    'HTI': 'HT',
    'MEX': 'MX',
    'ZWE': 'ZW',
    'LCA': 'LC',
    'IND': 'IN',
    'LVA': 'LV',
    'BTN': 'BT',
    'VCT': 'VC',
    'VNM': 'VN',
    'NOR': 'NO',
    'CZE': 'CZ',
    'ATF': 'TF',
    'ATG': 'AG',
    'FJI': 'FJ',
    'HND': 'HN',
    'MUS': 'MU',
    'DOM': 'DO',
    'LUX': 'LU',
    'ISR': 'IL',
    'FSM': 'FM',
    'PER': 'PE',
    'REU': 'RE',
    'IDN': 'ID',
    'VUT': 'VU',
    'MKD': 'MK',
    'COD': 'CD',
    'COG': 'CG',
    'ISL': 'IS',
    'GLP': 'GP',
    'ETH': 'ET',
    'COM': 'KM',
    'COL': 'CO',
    'NGA': 'NG',
    'TLS': 'TL',
    'TWN': 'TW',
    'PRT': 'PT',
    'MDA': 'MD',
    'GGY': 'GG',
    'MDG': 'MG',
    'ATA': 'AQ',
    'ECU': 'EC',
    'SEN': 'SN',
    'ESH': 'EH',
    'MDV': 'MV',
    'ASM': 'AS',
    'SPM': 'PM',
    'CUW': 'CW',
    'FRA': 'FR',
    'LTU': 'LT',
    'RWA': 'RW',
    'ZMB': 'ZM',
    'GMB': 'GM',
    'WLF': 'WF',
    'JEY': 'JE',
    'FRO': 'FO',
    'GTM': 'GT',
    'DNK': 'DK',
    'IMN': 'IM',
    'MAF': 'MF',
    'AUS': 'AU',
    'AUT': 'AT',
    'SJM': 'SJ',
    'VEN': 'VE',
    'PLW': 'PW',
    'KEN': 'KE',
    'TUR': 'TR',
    'ALB': 'AL',
    'OMN': 'OM',
    'TUV': 'TV',
    'ALA': 'AX',
    'BRN': 'BN',
    'TUN': 'TN',
    'RUS': 'RU',
    'BRB': 'BB',
    'BRA': 'BR',
    'CIV': 'CI',
    'SRB': 'RS',
    'GNQ': 'GQ',
    'USA': 'US',
    'QAT': 'QA',
    'WSM': 'WS',
    'AZE': 'AZ',
    'GNB': 'GW',
    'SWZ': 'SZ',
    'TON': 'TO',
    'CAN': 'CA',
    'UKR': 'UA',
    'KOR': 'KR',
    'AIA': 'AI',
    'CAF': 'CF',
    'CHE': 'CH',
    'CYP': 'CY',
    'BIH': 'BA',
    'SGP': 'SG',
    'SGS': 'GS',
    'SOM': 'SO',
    'UZB': 'UZ',
    'CMR': 'CM',
    'POL': 'PL',
    'KWT': 'KW',
    'ERI': 'ER',
    'GAB': 'GA',
    'CYM': 'KY',
    'ARE': 'AE',
    'EST': 'EE',
    'MWI': 'MW',
    'ESP': 'ES',
    'IRQ': 'IQ',
    'SLV': 'SV',
    'MLI': 'ML',
    'IRL': 'IE',
    'IRN': 'IR',
    'ABW': 'AW',
    'SLE': 'SL',
    'PAN': 'PA',
    'SDN': 'SD',
    'SLB': 'SB',
    'NZL': 'NZ',
    'MCO': 'MC',
    'ITA': 'IT',
    'JPN': 'JP',
    'KGZ': 'KG',
    'UGA': 'UG',
    'NCL': 'NC',
    'PNG': 'PG',
    'ARG': 'AR',
    'SWE': 'SE',
    'BHS': 'BS',
    'BHR': 'BH',
    'ARM': 'AM',
    'NRU': 'NR',
    'CUB': 'CU'
};