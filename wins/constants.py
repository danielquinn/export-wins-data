# Depending on how often these are edited, it may make more sense to put these
# into a model of their own, but as I don't have that information handy, I'm
# not going to over-complicate things at this stage for the sake of
# over-engineering.

# Also note that I've commented out DSO because I didn't sign up to sell
# weapons.  If you're comfortable with your helping DSO being on your
# conscience, then by all means, you can enable that here.  It's on you.

DSO = (
    (1, "DSO Head Office"),
    (2, "DSO Cyber Security Export Team"),
    (3, "DSO Business Development - Market Analysis"),
    (4, "DSO Director - Business Development - Events"),
    (5, "DSO - Business Development - Events"),
    (6, "DSO - Director - Business Development - Support to Business"),
    (7, "DSO - Head - Business Development - SME Team"),
    (8, "DSO - Business Development - Exportability"),
    (9, "DSO - Business Development - SME Team"),
    (10, "DSO - Business Development - Key Account Management"),
    (11, "DSO - Business Development - Mid Sized Businesses"),
    (12, "DSO - Director - RD1"),
    (13, "DSO - Deputy Director - RD 1"),
    (14, "DSO - RD 1A"),
    (15, "DSO - RD 1B"),
    (16, "DSO - RD 1C"),
    (17, "DSO - RD 1D"),
    (18, "DSO - RD 1E"),
    (19, "DSO - Director - RD2"),
    (20, "DSO - RD 2A"),
    (21, "DSO - Deputy Director - RD2"),
    (22, "DSO - RD 2B"),
    (23, "DSO - RD 2C"),
    (24, "DSO - RD 2D"),
    (25, "DSO - Senior Military Advisors"),
    (26, "DSO Policy and Resources"),
    (27, "DSO EM Exhibitions"),
    (28, "DSO Export Support Team (Bovington)"),
    (29, "DSO Export Support Team (Larkhill)"),
    (30, "DSO Director Business Development"),
)

EXPERIENCE = (
    (1, "Not yet exporting"),
    (2, "Last 12 months"),
    (3, "More than 1 year, less than 2"),
    (4, "More than 2 years, less than 5"),
    (5, "Over 5 years, less than 10"),
    (6, "More than 10 years"),
)

GOODS_VS_SERVICES = (
    (1, "Goods"),
    (2, "Services"),
    (3, "Goods and Services"),
)

HVO_PROGRAMMES = (
    (1, "(AER-01) Global Aerospace"),
    (2, "(AFB-01) Aid Funded Business Service"),
    (3, "(AUS-05) Australian Roads"),
    (4, "(AUS-06) Australia Airports"),
    (5, "(AZE-01) Azerbaijan Oil & Gas"),
    (6, "(BHR-01) Bahrain Rail"),
    (7, "(BRA-16) Shipyard & Shipbuilding Programme"),
    (8, "(BRA-18) Petrobras Business Plan 2013 - 2017"),
    (9, "(BRA-42) PPP Healthcare Programme"),
    (10, "(BRA-43) Brazilian Sports Infrastructure"),
    (11, "(BRA-44) Integrated Logistics"),
    (12, "(BRA-45) Brazilian Education"),
    (13, "(BRA-45) Brazilian Education"),
    (14, "(BRA-45) Brazilian Education"),
    (15, "(BSC-01) Big Science"),
    (16, "(BWA -01) Botswana Mining"),
    (17, "(BWA-01) Botswana Mining"),
    (18, "(CAN-01) Toronto Rail"),
    (19, "(CHL-12) Chile Mining"),
    (20, "(CHN-14) China Healthcare"),
    (21, "(CHN-20) China New Energy (Renewables)"),
    (22, "(CHN-20) China New Energy (Renewables)"),
    (23, "(CHN-21) China New Energy (Nuclear)"),
    (24, "(CHN-49) China Built Environment"),
    (25, "(CHN-51) China Airports"),
    (26, "(CHN-53) Chinese Commercial Aircraft Programmes"),
    (27, "(CHN-54) Clean And Energy Efficient Production"),
    (28, "(CHN-54) Clean And Energy Efficient Production"),
    (29, "(CHN-54) Clean and Energy Efficient Production"),
    (30, "(CHN-55) Technology Giants in China"),
    (31, "(CHN-55) Technology Giants in China"),
    (32, "(CHN-56) China Education"),
    (33, "(CHN-57) China Experience Economy"),
    (34, "(CHN-57) China Maritime"),
    (35, "(COL-02) Colombia Municipal infrastructure projects"),
    (36, "(COL-03) Colombia Multiple transport projects"),
    (37, "(COL-04) Colombian Education"),
    (38, "(COL-04) Colombian Education"),
    (39, "(COL-04) Colombian Education"),
    (40, "(COL-05) Colombia Mining"),
    (41, "(DNK-06) Femern Link Project"),
    (42, "(DZA-01) Algeria Healthcare"),
    (43, "(EAF-02) Kenya-Ethiopia Transport Corridor"),
    (44, "(EAK-01) Kenya Gas"),
    (45, "(EDU-01) Education"),
    (46, "(EDU-02) International Curriculum Schools"),
    (47, "(EDU-03) ASEAN Education & Training"),
    (48, "(EGY-01) Suez Canal Regional Development Project"),
    (49, "(ETH-01) Transport Corridor"),
    (50, "(EUR-02) Northern Europe Offshore Wind & Interconnector projects"),
    (51, "(EUR-02) Northern Europe Offshore Wind and Interconnetor projects"),
    (52, "(FRA-01) Big Science"),
    (53, "(FRA-01) Big Science"),
    (54, "(GIN - 01) Guinea Mining"),
    (55, "(GIN-01) Guinea Mining"),
    (56, "(GSC-01) Global Smart Cities"),
    (57, "(GSC-01) Global Smart Cities"),
    (58, "(GSC-01) Global Smart Cities"),
    (59, "(HJK-01) Jordan Nuclear New Build"),
    (60, "(HKG-01) Hong Kong Integrated Transport"),
    (61, "(HKG-05) Kai Tak Development"),
    (62, "(HKG-08) West Kowloon Cultural District"),
    (63, "(HKG-09) Zhuhai-Macao Bridge & Related Projects"),
    (64, "(HKG-15) Hong Kong Airport"),
    (65, "(HKG-16) Hong Kong Environment"),
    (66, "(HKG-17) Hong Kong Hospitals"),
    (67, "(HKG-18) Hong Kong Urban Regeneration & Built Heritage"),
    (68, "(INA-01) Indonesia Infrastructure"),
    (69, "(IND-03) Indian metro opportunities"),
    (70, "(IND-31) Conventional Power and Renewables"),
    (71, "(IND-32) Civil Nuclear"),
    (72, "(IND-50) Indian Industrial Corridors"),
    (73, "(IND-51) India Healthcare"),
    (74, "(IRQ-10) Iraq Oil & Gas"),
    (75, "(IRQ-11) Iraq Federal Water Projects"),
    (76, "(JPN-07) Fukushima Decommissioning"),
    (77, "(JPN-08) Japan - Major Sporting Events"),
    (78, "(KAZ - 07) Kazakhstan Mining"),
    (79, "(KAZ-02) Multiple Oil & Gas Projects"),
    (80, "(KAZ-03) Kazakhstan Infrastructure"),
    (81, "(KAZ-06) Kazakhstan Education"),
    (82, "(KAZ-06) Kazakhstan Education and Training"),
    (83, "(KAZ-06) Kazakhstan Education and Training"),
    (84, "(KAZ-07) Kazakhstan Mining"),
    (85, "(KOR-05) Global Sports Projects in Korea"),
    (86, "(KWT-01) Kuwait Airport Redevelopment"),
    (87, "(KWT-02) Boubyan Island Development"),
    (88, "(KWT-03) New Hospitals Project"),
    (89, "(KWT-04) Kuwait Metro System"),
    (90, "(LBY-01) Libya Infrastructure"),
    (91, "(LBY-02) Libya Healthcare"),
    (92, "(LBY-03) Libya Water"),
    (93, "(LBY-04) Libya Airports"),
    (94, "(MAC-01) Macau Retail & Leisure"),
    (95, "(MEX-04) Mexico Oil and Gas"),
    (96, "(MEX-05) Mexican Education"),
    (97, "(MEX-05) Mexican Education"),
    (98, "(Mex-05) Mexican Education"),
    (99, "(MEX-07) Veracruz Port Expansion"),
    (100, "(MEX-08) Mexico Airports"),
    (101, "(MIN-01) Global Mining Supply Chains"),
    (102, "(MIN-02) Energy for the West African Mining Industry (West African Power Pool/WAPP)"),
    (103, "(MOR-01) Morocco Mining"),
    (104, "(MOZ-01) Mozambique Gas"),
    (105, "(MYS-06) Malaysian Transport Projects"),
    (106, "(MYS-07) Malaysia Education"),
    (107, "(NGA-05) Nigeria Oil & Gas projects"),
    (108, "(NOR-01) Oil & Gas Norway"),
    (109, "(NUC-01) Central European Nuclear"),
    (110, "(NUC-04) Nuclear Vendor Strategy"),
    (111, "(NUC-05) Western Europe Decommissioning"),
    (112, "(NZl-01) Christchurch Reconstruction"),
    (113, "(OAG-01) East Africa Oil & Gas"),
    (114, "(OMN-01) Omani Railway Network"),
    (115, "(OMN-05) OMAN Healthcare"),
    (116, "(OTH-11) Aid Funded Business Service"),
    (117, "(OTH-11) Aid Funded Business Service"),
    (118, "(OTH-12) Building Creative Hubs Internationally"),
    (119, "(OTH-12) Building Creative Hubs Internationally"),
    (120, "(OTH-13) Creative Industries HVO Taskforce"),
    (121, "(OTH-13) Creative Industries HVO Taskforce"),
    (122, "(OTH-14) Creative Tax Credits"),
    (123, "(OTH-14) Creative Tax Credits"),
    (124, "(OTH-15) Food and Drink Export Action Plan"),
    (125, "(OTH-15) Food and Drink Export Action Plan"),
    (126, "(OTH-16) Free Trade Agreements"),
    (127, "(OTH-18) Global E Retail (Digital Export Growth) Programme"),
    (128, "(OTH-18) Global E Retail (Digital Export Growth) Programme"),
    (129, "(OTH-22) UK Retail Industry - International Action Plan"),
    (130, "(OTH-22) UK Retail Industry - International Action Plan"),
    (131, "(PAN-01) Panama Canal Megaprojects"),
    (132, "(PAN-02) Panama City Metro Lines 2 and 3"),
    (133, "(PER-01) Peru Mass Rapid Transport System"),
    (134, "(PER-03) Peru Mining"),
    (135, "(PER-04 )Lima 2019 Pan-American Games"),
    (136, "(PHL-09) PPP Infrastructure Projects"),
    (137, "(POL-01) Polish Rail"),
    (138, "(QAT-04) Qatari Rail Network"),
    (139, "(QAT-06) World Cup 2022"),
    (140, "(QAT-07) Qatari National Food Security Programme"),
    (141, "(QAT-07) Qatari National Food Security Programme"),
    (142, "(QAT-08) Qatar Education and Training"),
    (143, "(QAT-08) Qatar Education and Training"),
    (144, "(QAT-08) Qatar Education and Training"),
    (145, "(REN-01) Northern Europe Offshore Wind & Interconnector Projects"),
    (146, "(RUS-50) Russian Sports Infrastructure Projects"),
    (147, "(RUS-52) Russia Oil"),
    (148, "(RUS-54) Russia Experience Economy"),
    (149, "(RUS-54) Russia Experience Economy"),
    (150, "(SAU-06) Saudi Railways Development Programme"),
    (151, "(SAU-08) Healthcare Development Programme"),
    (152, "(SAU-15) Saudi Airport Developments"),
    (153, "(SAU-17) Saudi Water Projects"),
    (154, "(SAU-19) Saudi Arabia Oil & Gas"),
    (155, "(SAU-20) Saudi Nuclear - New Build"),
    (156, "(SAU-21) Saudi Education"),
    (157, "(SAU-21) Saudi Education"),
    (158, "(SAU-21) Saudi Education"),
    (159, "(SAU-22) Jeddah Urban Redevelopment Programme"),
    (160, "(SGP-06) Mass Rapid Transport"),
    (161, "(SGP-07) Changi Airport"),
    (162, "(SGP-08) Singapore Water"),
    (163, "(SPO-01) Central Asia Major Sports Events"),
    (164, "(SSA-01) Angola Oil & Gas"),
    (165, "(TGA-01) Technology Giants in SE Asia"),
    (166, "(TGA-01) Technology Giants in SE Asia"),
    (167, "(TGU-01) Technology Giants in the USA"),
    (168, "(TGU-01) Technology Giants in the USA"),
    (169, "(THA-01) Flood Management & Transport Infrastructure"),
    (170, "(THA-10) Thailand Rail & Airport"),
    (171, "(TUR-26) Turkey Nuclear New Build"),
    (172, "(TUR-27) Istanbul Airport"),
    (173, "(TUR-28) PPP & Healthcare"),
    (174, "(TWN-15) Rail Projects"),
    (175, "(TWN-19) Taiwan Renewables"),
    (176, "(TWN-19) Taiwan Renewables"),
    (177, "(TWN-20) Taiwan Nuclear"),
    (178, "(TZA-01) Tanzania Gas"),
    (179, "(UAE-04) UAE Rail Project"),
    (180, "(UAE-05) UAE Experience Economy"),
    (181, "(UAE-12) UAE Healthcare"),
    (182, "(UAE-13) UAE Expo 2020"),
    (183, "(UAE-19) Dubai Airport Expansion"),
    (184, "(UAE-20) UAE Education"),
    (185, "(UAE-27)"),
    (186, "(UGA-01) Uganda Gas"),
    (187, "(USA-26) US Water Sector Capital Improvement Program/Plan"),
    (188, "(USA-31) US Infrastructure"),
    (189, "(USA-31) US Infrastructure"),
    (190, "(VNM-30) Vietnam Urban Regeneration and Transport Projects"),
    (191, "(VNM-31) Vietnam Nuclear New Build"),
)

INVESTMENTS = (
    (1, "ITFG - E-Business Projects Team"),
    (2, "ITFG - Overseas Resources Team"),
    (3, "ITFG - ICT & Data Policy and Support"),
    (4, "ITFG - E-Business Operational Support Team"),
    (5, "ITFG - Director ITFG & PA"),
    (6, "ITFG - Finance Team"),
    (7, "ITFG - Business Planning Team"),
    (8, "IG - Regeneration Investment Organisation (RIO)"),
    (9, "IG - Global Accounts - Director & Deputy Director & PA"),
    (10, "IG - Global Accounts - IT Software & Creative"),
    (11, "IG - Global Accounts - Electronics & Communications"),
    (12, "IG - Global Accounts - Financial & Business Services"),
    (13, "IG - Global Accounts - Energy & Infrastructure"),
    (14, "IG - Global Accounts - Adv Man - Auto, Rail MEPE"),
    (15, "IG - Global Accounts - Adv Man - Aero, Space, Chem"),
    (16, "IG - Global Accounts - Life Science, Agri- Tech"),
    (17, "IG - Global Operations - Global Entrepreneurs Programme"),
    (18, "IG - Global Operations - Graduate Entrepreneurs"),
    (19, "IG - Global Operations - Network Linkages & Professional Development"),
    (20, "IG - Global Operations - In Market Strategies & Development"),
    (21, "IG - Strategy/Policy/Local Engagement - Director & PA"),
    (22, "IG - Strategy/Policy/Local Engagement - Strategy"),
    (23, "IG - Strategy/Policy/Local Engagement - Global Intelligence"),
    (24, "IG - Strategy/Policy/Local Engagement - Local Engagement & Delivery"),
    (25, "IG - Strategy/Policy/Local Engagement - National & Local Policy"),
    (26, "IG - Specialists - Advanced Manufacturing"),
    (27, "IG - Specialists - Knowledge Intensive Industry"),
    (28, "IG - Specialists - Energy & Infrastructure"),
    (29, "IG - Specialists - Life Sciences"),
    (30, "IG - Finance & Business Planning"),
    (31, "IG - Global Intelligence Unit"),
    (32, "IG - SR - Strategic Accounts"),
    (33, "IG - SR - Institutional Investment"),
    (34, "IG - Global Operations - FDI Projects - Advanced Engineering"),
    (35, "IG - Global Operations - Director & PA"),
    (36, "IG - Global Operations - FDI Projects - Energy and Infrastructure"),
    (37, "IG - Global Operations - Briefing Tours and Visits"),
    (38, "IG - Global Operations and Network Performance"),
    (39, "IG - Global Operations - Deputy Director"),
    (40, "IG - Global Operations - Shared Services"),
    (41, "IG - UKAN Involvement"),
    (42, "IG - Strategy & Policy - Resources and Finance"),
    (43, "IG - Strategy & Policy - FDI Projects - Financial Services"),
    (44, "IG - Strategy & Policy - FDI Contract - Networks & Partnerships"),
    (45, "IG - Strategy & Policy - Investor Policy"),
    (46, "IG - Strategy & Policy - Briefing Tours and Visits"),
    (47, "IG - Strategy & Policy - Director & PA"),
    (48, "IG - Strategy & Policy - FDI Projects - Electronics and Comms"),
    (49, "IG - Strategy & Policy - Deputy Director"),
    (50, "IG - Strategy & Policy - Information Hub"),
    (51, "IG - Strategy & Policy - Local Policy & Engagement - DAs & Eng"),
    (52, "IG - CPI - FDI Projects - Life Sciences - Food & Drink"),
    (53, "IG - CPI - FDI Projects - New Technologies"),
    (54, "IG - Campaigns and Special Programmes"),
    (55, "IG - Tech City Investment Organisation"),
)

OTHER_HQ_TEAM = (
    (1, "UKTI Education"),
    (2, "Healthcare UK"),
    (3, "Offshore Wind Investment Organisation"),
    (4, "Tech City Project"),
    (5, "BG - Tech City"),
    (6, "Financial Services Organisation (FSO)"),
)

PROGRAMMES = (
    (1, "Afterburner"),
    (2, "Aid Funded Business Service (AFBS)"),
    (3, "Britain Open for Business"),
    (4, "British Business Network"),
    (5, "British Defence Staff - US"),
    (6, "Business Win FCO Involvement"),
    (7, "Catalyst Members Activities"),
    (8, "CEN Adv Engineering"),
    (9, "CEN Adv Manufacturing"),
    (10, "CEN Defence & Security"),
    (11, "CEN Energy"),
    (12, "CEN Health & Life Science"),
    (13, "CEN Infrastructure"),
    (14, "CEN Life Science"),
    (15, "CEN Security"),
    (16, "CEN Services"),
    (17, "Commonwealth Games"),
    (18, "Digital Trade Advisor"),
    (19, "E-Exporting"),
    (20, "Emerging Markets Contract (CEE)"),
    (21, "Emerging Markets Contract (Gulf)"),
    (22, "Emerging Markets Contract (LA)"),
    (23, "Emerging Markets Contract (Russia)"),
    (24, "Events Alliance"),
    (25, "Export Communication Review Scheme (ECR)"),
    (26, "Export Growth Service"),
    (27, "Export Oriented FDI"),
    (28, "Exporting is GREAT (EiG)"),
    (29, "EY Specialist Business Win"),
    (30, "First Time Exporters Programme"),
    (31, "Free Trade Agreements"),
    (32, "GCP"),
    (33, "GCP - Deloitte"),
    (34, "GCP - EY"),
    (35, "GCP - HSBC"),
    (36, "GCP - KPMG"),
    (37, "GCP - Lloyds"),
    (38, "GCP - PwC"),
    (39, "GCP - RBS"),
    (40, "GCP - Santander"),
    (41, "GCP - Standard Chartered"),
    (42, "GREAT Branded Event Great Campaign"),
    (43, "GREAT Challenge Fund"),
    (44, "GREAT Funded Activity"),
    (45, "GREAT Weeks"),
    (46, "Grown in Britain Global Business Programme"),
    (47, "HVO Specialist [involvement]"),
    (48, "III - Deal Ticket Size"),
    (49, "Innovation Programme"),
    (50, "International Festival for Business"),
    (51, "JETCO"),
    (52, "Low Carbon Initiative"),
    (53, "Luxury Retail"),
    (54, "Milan Expo 2015"),
    (55, "MSB Programme"),
    (56, "Music Export Growth Scheme (MEGS)"),
    (57, "Northern Powerhouse (NPH)"),
    (58, "Offshore Wind Investment Organisation"),
    (59, "Olympics 2012"),
    (60, "Overseas Market Introduction Service (OMIS)"),
    (61, "PA Specialist Business Win"),
    (62, "Reshore UK"),
    (63, "Rugby World Cup - Business Festival"),
    (64, "Shakespeare Lives"),
    (65, "Stakeholder Engagement"),
    (66, "Technology Strategy Board (TSB)"),
    (67, "UK Israel Tech Hub"),
    (68, "Venture Capital"),
    (69, "Web-based Exporting Programme"),
)

RATINGS = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "N/A"),
)

SECTORS = (
    (1, "Advanced Engineering"),
    (2, "Aerospace"),
    (3, "Aerospace : Aircraft Design"),
    (4, "Aerospace : Component Manufacturing"),
    (5, "Aerospace : Component Manufacturing : Engines"),
    (6, "Aerospace : Component Manufacturing : test widgerts"),
    (7, "Aerospace : Maintenance"),
    (8, "Aerospace : Manufacturing and Assembly"),
    (9, "Aerospace : Manufacturing and Assembly : Aircraft"),
    (10, "Aerospace : Manufacturing and Assembly : Helicopters"),
    (11, "Aerospace : Manufacturing and Assembly : Space Technology"),
    (12, "Aerospace : Manufacturing and Assembly : UAVs"),
    (13, "Agriculture, Horticulture and Fisheries"),
    (14, "Airports"),
    (15, "Automotive"),
    (16, "Automotive : Automotive Maintenance"),
    (17, "Automotive : Automotive Retail"),
    (18, "Automotive : Component Manufacturing"),
    (19, "Automotive : Component Manufacturing : Bodies and Coachwork"),
    (20, "Automotive : Component Manufacturing : Electronic Components"),
    (21, "Automotive : Component Manufacturing : Engines and Transmission"),
    (22, "Automotive : Component Manufacturing : Tyres"),
    (23, "Automotive : Design Engineering"),
    (24, "Automotive : Manufacturing and Assembly"),
    (25, "Automotive : Manufacturing and Assembly : Agricultural Machinery"),
    (26, "Automotive : Manufacturing and Assembly : Bicycles"),
    (27, "Automotive : Manufacturing and Assembly : Caravans"),
    (28, "Automotive : Manufacturing and Assembly : Cars"),
    (29, "Automotive : Manufacturing and Assembly : Containers"),
    (30, "Automotive : Manufacturing and Assembly : Invalid Carriages"),
    (31, "Automotive : Manufacturing and Assembly : Lorries"),
    (32, "Automotive : Manufacturing and Assembly : Motorcycles"),
    (33, "Automotive : Manufacturing and Assembly : Trailers"),
    (34, "Automotive : Manufacturing and Assembly : Vans"),
    (35, "Automotive : Motorsport"),
    (36, "Biotechnology and Pharmaceuticals"),
    (37, "Biotechnology and Pharmaceuticals : Bio and Pharma Marketing and Sales"),
    (38, "Biotechnology and Pharmaceuticals : Bio and Pharma Marketing and Sales : Bio and Pharma Retail"),
    (39, "Biotechnology and Pharmaceuticals : Bio and Pharma Marketing and Sales : Bio and Pharma Wholesale"),
    (40, "Biotechnology and Pharmaceuticals : Biotechnology"),
    (41, "Biotechnology and Pharmaceuticals : Biotechnology : Agribio"),
    (42, "Biotechnology and Pharmaceuticals : Biotechnology : Biodiagnostics"),
    (43, "Biotechnology and Pharmaceuticals : Biotechnology : Biomanufacturing"),
    (44, "Biotechnology and Pharmaceuticals : Biotechnology : Bioremediation"),
    (45, "Biotechnology and Pharmaceuticals : Biotechnology : Biotherapeutics"),
    (46, "Biotechnology and Pharmaceuticals : Biotechnology : Industrialbio"),
    (47, "Biotechnology and Pharmaceuticals : Biotechnology : Platform Technologies"),
    (48, "Biotechnology and Pharmaceuticals : Clinical Trials"),
    (49, "Biotechnology and Pharmaceuticals : Lab Services"),
    (50, "Biotechnology and Pharmaceuticals : Lab Services : Contract Research"),
    (51, "Biotechnology and Pharmaceuticals : Lab Services : Reagents, Consumables and Instruments"),
    (52, "Biotechnology and Pharmaceuticals : Pharmaceuticals"),
    (53, "Biotechnology and Pharmaceuticals : Pharmaceuticals : Basic Pharmaceutical Products"),
    (54, "Biotechnology and Pharmaceuticals : Pharmaceuticals : Drug Discovery"),
    (55, "Biotechnology and Pharmaceuticals : Pharmaceuticals : Drug Manufacture"),
    (56, "Biotechnology and Pharmaceuticals : Pharmaceuticals : Neutraceuticals"),
    (57, "Biotechnology and Pharmaceuticals : Vaccines"),
    (58, "Business (and Consumer) Services"),
    (59, "Business (and Consumer) Services : Commercial Real Estate Services"),
    (60, "Business (and Consumer) Services : Contact Centres"),
    (61, "Business (and Consumer) Services : HR Services"),
    (62, "Business (and Consumer) Services : Marketing Services"),
    (63, "Business (and Consumer) Services : Marketing Services : Market Research"),
    (64, "Business (and Consumer) Services : Shared Service Centres"),
    (65, "Chemicals"),
    (66, "Chemicals : Agricultural Chemicals"),
    (67, "Chemicals : Basic Chemicals"),
    (68, "Chemicals : Cleaning Preparations"),
    (69, "Chemicals : Miscellaneous Chemicals"),
    (70, "Chemicals : Paint, Coating and Adhesive Products"),
    (71, "Chemicals : Synthetic Materials"),
    (72, "Clothing, Footwear and Fashion"),
    (73, "Clothing, Footwear and Fashion : Clothing"),
    (74, "Clothing, Footwear and Fashion : Clothing : Workwear"),
    (75, "Clothing, Footwear and Fashion : Footwear"),
    (76, "Communications"),
    (77, "Communications : Broadband"),
    (78, "Communications : Communications Wholesale"),
    (79, "Communications : Convergent"),
    (80, "Communications : Fixed Line"),
    (81, "Communications : Mobile"),
    (82, "Communications : Mobile : 3G Services"),
    (83, "Communications : Mobile : GSM"),
    (84, "Communications : Retail"),
    (85, "Communications : Wireless"),
    (86, "Communications : Wireless : Wi-Fi"),
    (87, "Communications : Wireless : Wi-Max"),
    (88, "Construction"),
    (89, "Creative and Media"),
    (90, "Creative and Media : Architecture"),
    (91, "Creative and Media : Art, Design and Creativity"),
    (92, "Creative and Media : Art, Design and Creativity : Artistic and Literary Creation"),
    (93, "Creative and Media : Art, Design and Creativity : Arts Facilities Operation"),
    (94, "Creative and Media : Art, Design and Creativity : Design"),
    (95, "Creative and Media : Art, Design and Creativity : Fashion"),
    (96, "Creative and Media : Art, Design and Creativity : Live Theatrical Presentations"),
    (97, "Creative and Media : Creative and Media Distribution"),
    (98, "Creative and Media : Creative and Media Distribution : Film and Video"),
    (99, "Creative and Media : Creative and Media Equipment"),
    (100, "Creative and Media : Creative and Media Equipment : Musical Instrument Manufacture"),
    (101, "Creative and Media : Creative and Media Equipment : Photo and Cinema Equipment"),
    (102, "Creative and Media : Creative and Media Retail"),
    (103, "Creative and Media : Creative and Media Retail : Antiques and Antiquities"),
    (104, "Creative and Media : Creative and Media Retail : Art"),
    (105, "Creative and Media : Creative and Media Retail : Books, Newspapers and Stationery"),
    (106, "Creative and Media : Creative and Media Wholesaling"),
    (107, "Creative and Media : Creative and Media Wholesaling : Multimedia Sales"),
    (108, "Creative and Media : Creative and Media Wholesaling : Musical Instruments"),
    (109, "Creative and Media : Creative and Media Wholesaling : Photographic Goods"),
    (110, "Creative and Media : Events and Attractions"),
    (111, "Creative and Media : Media"),
    (112, "Creative and Media : Media : Advertising"),
    (113, "Creative and Media : Media : Film, Photography and Animation"),
    (114, "Creative and Media : Media : Music"),
    (115, "Creative and Media : Media : Publishing"),
    (116, "Creative and Media : Media : TV and Radio"),
    (117, "Creative and Media : Media : Video Games"),
    (118, "Creative and Media : Media Reproduction"),
    (119, "Creative and Media : Media Reproduction : Printing"),
    (120, "Creative and Media : Media Reproduction : Reproduction"),
    (121, "Defence"),
    (122, "Defence and Security"),
    (123, "Education and Training"),
    (124, "Electronics and IT Hardware"),
    (125, "Electronics and IT Hardware : Electronic Instruments"),
    (126, "Electronics and IT Hardware : Electronics and IT Technologies"),
    (127, "Electronics and IT Hardware : Electronics and IT Technologies : Broadcasting"),
    (128, "Electronics and IT Hardware : Electronics and IT Technologies : Component Technologies"),
    (129, "Electronics and IT Hardware : Electronics and IT Technologies : Computing"),
    (130, "Electronics and IT Hardware : Electronics and IT Technologies : Display Technologies"),
    (131, "Electronics and IT Hardware : Electronics and IT Technologies : Network Technologies"),
    (132, "Electronics and IT Hardware : Electronics and IT Technologies : Security Technologies"),
    (133, "Energy"),
    (134, "Environment"),
    (135, "Environment : Air Pollution and Noise Control"),
    (136, "Environment : Environmental Monitoring"),
    (137, "Environment : Fuel Cells"),
    (138, "Environment : Marine Pollution Control"),
    (139, "Environment : Sanitation and Remediation"),
    (140, "Environment : Waste Management"),
    (141, "Environment : Waste Management : Hazardous Waste Management"),
    (142, "Environment : Waste Management : Non-Metal Waste and Scrap Recycling"),
    (143, "Environment : Waste Management : Sewage Collection and Treatment"),
    (144, "Environment : Waste to Energy"),
    (145, "Environment : Water Management"),
    (146, "Environment and Water"),
    (147, "Financial Services (including Professional Services)"),
    (148, "Financial Services (including Professional Services) : Asset Management"),
    (149, "Financial Services (including Professional Services) : Banking"),
    (150, "Financial Services (including Professional Services) : Banking : Commercial Banking"),
    (151, "Financial Services (including Professional Services) : Banking : Investment Banking"),
    (152, "Financial Services (including Professional Services) : Banking : Private Banking"),
    (153, "Financial Services (including Professional Services) : Banking : Retail Banking"),
    (154, "Financial Services (including Professional Services) : Capital Markets"),
    (155, "Financial Services (including Professional Services) : Capital Markets : Hedge Funds"),
    (156, "Financial Services (including Professional Services) : Capital Markets : Private Equity"),
    (157, "Financial Services (including Professional Services) : Capital Markets : Venture Capital"),
    (158, "Financial Services (including Professional Services) : Foreign Exchange"),
    (159, "Financial Services (including Professional Services) : Insurance"),
    (160, "Financial Services (including Professional Services) : Insurance : Commercial Insurance"),
    (161, "Financial Services (including Professional Services) : Insurance : Home Insurance"),
    (162, "Financial Services (including Professional Services) : Insurance : Life Insurance"),
    (163, "Financial Services (including Professional Services) : Insurance : Motor Insurance"),
    (164, "Financial Services (including Professional Services) : Insurance : Travel Insurance"),
    (165, "Financial Services (including Professional Services) : Listings"),
    (166, "Financial Services (including Professional Services) : Professional Services"),
    (167, "Financial Services (including Professional Services) : Professional Services : Accountancy Services"),
    (168, "Financial Services (including Professional Services) : Professional Services : Legal Services"),
    (169, "Financial Services (including Professional Services) : Professional Services : Management Consultancy"),
    (170, "Food and Drink"),
    (171, "Food and Drink : Bakery Products"),
    (172, "Food and Drink : Beverages and Alcoholic Drinks"),
    (173, "Food and Drink : Brewing"),
    (174, "Food and Drink : Dairy Products"),
    (175, "Food and Drink : Food and Drink Manufacturing"),
    (176, "Food and Drink : Frozen and Chilled Foods"),
    (177, "Food and Drink : Fruit and Vegetables"),
    (178, "Food and Drink : Meat Products"),
    (179, "Food and Drink : Pet Food"),
    (180, "Food and Drink : Ready Meals"),
    (181, "Food and Drink : Secondary Food Processing"),
    (182, "Food and Drink : Tobacco Products"),
    (183, "Giftware, Jewellery and Tableware"),
    (184, "Global Sports Projects"),
    (185, "Global Sports Projects : Major Events"),
    (186, "Healthcare and Medical"),
    (187, "Healthcare and Medical : Healthcare Marketing and Sales"),
    (188, "Healthcare and Medical : Healthcare Marketing and Sales : Healthcare Retail"),
    (189, "Healthcare and Medical : Healthcare Marketing and Sales : Healthcare Wholesale"),
    (190, "Healthcare and Medical : Healthcare Services"),
    (191, "Healthcare and Medical : Healthcare Services : Dentists"),
    (192, "Healthcare and Medical : Healthcare Services : Medical Practice"),
    (193, "Healthcare and Medical : Healthcare Services : Nursing Homes"),
    (194, "Healthcare and Medical : Healthcare Services : Private Sector"),
    (195, "Healthcare and Medical : Healthcare Services : Public Sector"),
    (196, "Healthcare and Medical : Healthcare Services : Vets"),
    (197, "Healthcare and Medical : Medical Consumables"),
    (198, "Healthcare and Medical : Medical Devices and Systems"),
    (199, "Healthcare and Medical : Medical Devices and Systems : Optical Precision Instruments"),
    (200, "Healthcare and Medical : Medical Equipment"),
    (201, "Healthcare and Medical : Medical Equipment : Dental Aesthetics"),
    (202, "Healthcare and Medical : Medical Equipment : Glass"),
    (203, "Healthcare and Medical : Medical Equipment : Spectacles and Unmounted Lenses"),
    (204, "Healthcare and Medical : Medical Lab Services"),
    (205, "Household Goods, Furniture and Furnishings"),
    (206, "ICT"),
    (207, "Leisure and Tourism"),
    (208, "Leisure and Tourism : Gaming"),
    (209, "Leisure and Tourism : Gaming : Casino Gambling"),
    (210, "Leisure and Tourism : Gaming : Mass-Market Gambling"),
    (211, "Leisure and Tourism : Sports and Leisure Infrastructure"),
    (212, "Life Sciences"),
    (213, "Marine"),
    (214, "Mass Transport"),
    (215, "Mechanical Electrical and Process Engineering"),
    (216, "Metallurgical Process Plant"),
    (217, "Metals, Minerals and Materials"),
    (218, "Metals, Minerals and Materials : Ceramics"),
    (219, "Metals, Minerals and Materials : Composite Materials"),
    (220, "Metals, Minerals and Materials : Elastomers and Rubbers"),
    (221, "Metals, Minerals and Materials : Metals"),
    (222, "Metals, Minerals and Materials : Minerals"),
    (223, "Metals, Minerals and Materials : Plastics"),
    (224, "Mining"),
    (225, "More Sectors"),
    (226, "Oil and Gas"),
    (227, "Ports and Logistics"),
    (228, "Power"),
    (229, "Power : Nuclear"),
    (230, "Power : Nuclear : Nuclear De-commissiong"),
    (231, "Railways"),
    (232, "Renewable Energy"),
    (233, "Renewable Energy : Biomass"),
    (234, "Renewable Energy : Geothermal"),
    (235, "Renewable Energy : Hydro"),
    (236, "Renewable Energy : Solar"),
    (237, "Renewable Energy : Tidal"),
    (238, "Renewable Energy : Wave"),
    (239, "Renewable Energy : Wind"),
    (240, "Renewable Energy : Wind : Renewable energy: Wind: Offshore"),
    (241, "Renewable Energy : Wind : Renewable energy: Wind: Onshore"),
    (242, "Retail"),
    (243, "Security"),
    (244, "Security : Cyber Security"),
    (245, "Software and Computer Services Business to Business (B2B)"),
    (246, "Software and Computer Services Business to Business (B2B) : Biometrics"),
    (247, "Software and Computer Services Business to Business (B2B) : E-Procurement"),
    (248, "Software and Computer Services Business to Business (B2B) : Financial Applications"),
    (249, "Software and Computer Services Business to Business (B2B) : Healthcare Applications"),
    (250, "Software and Computer Services Business to Business (B2B) : Industry Applications"),
    (251, "Software and Computer Services Business to Business (B2B) : Online Retailing"),
    (252, "Software and Computer Services Business to Business (B2B) : Security Related Software"),
    (253, "Software and Computer Services Business to Business (B2B) : Support Services"),
    (254, "Software and Computer Services Business to Business (B2B) : Support Services : Equipment Maintenance and Repair"),
    (255, "Software and Computer Services Business to Business (B2B) : Support Services : Internet Service Providers"),
    (256, "Textiles, Interior Textiles and Carpets"),
    (257, "Water"),
)

TEAMS = (
    (1, "Trade (TD or ST)"),
    (2, "Investment (ITFG or IG)"),
    # (3, "DSO"),
    (4, "Other HQ Team"),
    (5, "UK Region"),
    (6, "Overseas Post"),
)

TRADES = (
    (1, "TD - Events - Financial & Professional Business Services"),
    (2, "TD - Events - Education"),
    (3, "TD - Events - Services"),
    (4, "TD - Events - Creative Industries"),
    (5, "TD - Events - Retail"),
    (6, "TD - Events - Large Events Support"),
    (7, "TD - Events - Rapid Response"),
    (8, "TD - Events - Large Events"),
    (9, "TD - Events - Venture Capital"),
    (10, "TD - Events - Energy"),
    (11, "TD - Events - Advanced Manufacturing"),
    (12, "TD - Events - Advanced Engineering"),
    (13, "TD - Events - Agrifood"),
    (14, "TD - Events - Consumer Goods"),
    (15, "TD - Events - Marine"),
    (16, "TD - Events - Advanced Manufacturing - Support"),
    (17, "TD - Events - Planning and Procurement"),
    (18, "TD - Finance & Performance"),
    (19, "TD - Technology, Innovation and Events - Venture Capital Unit"),
    (20, "TD - Technology, Innovation and Events - Science and Innovation"),
    (21, "TD - Technology, Innovation and Events - Technology Partnerships"),
    (22, "TD - Technology, Innovation and Events - Open to Export"),
    (23, "TD - Technology, Innovation and Events"),
    (24, "TD - Events Delivery & Performance"),
    (25, "TD - Events - BDV"),
    (26, "TD - Events - Markets"),
    (27, "TD - TAP Team"),
    (28, "TD - Business Development"),
    (29, "TD - Events - Sport"),
    (30, "TD - Events - Infrastructure & Life Sciences"),
    (31, "TD - Events - Infrastructure"),
    (32, "TD - Infrastructure & Life Sciences"),
    (33, "TD - Events - ICT"),
    (34, "TD - Events - Transport"),
    (35, "TD - Events - Healthcare"),
    (36, "TD - Events - Construction"),
    (37, "TD - Events - Open to Export"),
    (38, "ST - Managing Director and PA"),
    (39, "ST - Infrastructure and Life Science - Healthcare Pharma and Bio"),
    (40, "ST - Infrastructure & Life Science - Construction/Mass Transport"),
    (41, "ST - Infrastructure and Life Science - Low Carbon Env Water"),
    (42, "ST - Infrastructure and Life Science - High Value Opportunities"),
    (43, "ST - Infrastructure and Life Science - Support Team"),
    (44, "ST - Infrastructure and Life Science - Sport"),
    (45, "ST - High Value Opportunities Activities"),
    (46, "ST - Service Industries - Education and Experience Economy"),
    (47, "ST - Service Industries - Financial Professional and Business"),
    (48, "ST - Service Industries - Retail and Lifestyle"),
    (49, "ST - Service Industries - Agri-Food Drink & Aid Funded Business"),
    (50, "ST - Director - Service Industries"),
    (51, "ST - Service Industries - Support Team"),
    (52, "ST - Service Industries - Creative Industries"),
    (53, "ST - Advanced Manufacturing - Support Team"),
    (54, "ST - Advanced Manufacturing - Advanced Engineering"),
    (55, "ST - Advanced Manufacturing - ICT"),
    (56, "ST - Advanced Manufacturing - Energy"),
    (57, "ST - Middle East"),
    (58, "ST - Central and Latin America"),
    (59, "ST - Russia - Turkey - Central Asia"),
    (60, "ST - Africa"),
    (61, "ST - Dir - Emerging Markets - China - Southern Asia"),
    (62, "ST - Emerging Markets - China - Southern Asia - Support"),
    (63, "ST - Emerging Markets"),
    (64, "ST - China"),
    (65, "ST - South Asia"),
    (66, "ST - South East Asia"),
    (67, "ST - Dir - Developed Markets"),
    (68, "ST - Developed Markets - Support Team"),
    (69, "ST - North America - East Asia - Australasia - Caribbean"),
    (70, "ST - Europe"),
    (71, "ST - Group Resources - Support Team"),
)

TYPES = (
    (1, "Export Win"),
    (2, "Non-Export Win"),
    (3, "Mixed - Export and Non-Export Wins"),
)

TYPES_OF_SUPPORT = (
    (1, "Market entry advice and support – UKTI/FCO in UK"),
    (2, "Missions, tradeshows and events (UKTI/FCO)"),
    (3, "Advice, access and contacts – UKTI/FCO Overseas"),
    (4, "Political and economic briefing"),
    (5, "Lobbying to overcome a problem – UKTI/FCO"),
    (6, "Building positive reputation – UKTI/FCO"),
    (7, "Non-export : Outward Direct Investment – FCO"),
    (8, "Non-export : Reduced tax burdens – FCO"),
    (9, "Non-export : New Business in UK/3rd market – FCO"),
    (10, "Non-export : Other – FCO"),
)

UK_REGIONS = (
    (1, "East Midlands"),
    (2, "East of England"),
    (3, "London"),
    (4, "North East"),
    (5, "North West"),
    (6, "Northern Ireland"),
    (7, "Scotland"),
    (8, "South East"),
    (9, "South West"),
    (10, "Wales"),
    (11, "West Midlands"),
    (12, "Yorkshire and The Humber"),
)

WITHOUT_OUR_SUPPORT = (
    (1, "Would not have achieved any value"),
    (2, "1% – 20%"),
    (3, "21% - 40%"),
    (4, "41% - 60%"),
    (5, "61% - 80%"),
    (6, "81% - 99%"),
    (7, "All of it, the value would have been similar"),
)
