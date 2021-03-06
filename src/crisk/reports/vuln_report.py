#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009 José de Paula Eufrásio Júnior <jose.junior@gmail.com>

#    This file is part of Crisk.
#
#    Crisk is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Crisk is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Crisk.  If not, see <http://www.gnu.org/licenses/>.

import os
import gettext

from geraldo import *
from geraldo.generators import PDFGenerator
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from crisk.model import *
from crisk.reports.graphs import VulnGraph 

_ = gettext.gettext

class BandHeader(ReportBand):
    height = 1.5*cm
    elements = [
                Label(text=_('Total Vulnerability Report'), 
                            width = 13*cm,
                            style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 16 }),
                Label(text = _('Vulnerability'), top = 1*cm, left = 0.5*cm,
                      style = {'fontName' : 'Helvetica-Bold'}),
                Label(text = _('Severity'), top = 1*cm, left = 11*cm,
                      style = {'fontName' : 'Helvetica-Bold'}),
                Label(text = _('Probability'), top = 1*cm, bottom = 0.3*cm, left = 13*cm,
                      style = {'fontName' : 'Helvetica-Bold'}),
                Label(text = _('Risk'), top = 1*cm, bottom = 0.3*cm, left = 16*cm,
                      style = {'fontName' : 'Helvetica-Bold'})
                ]
    borders = {'bottom' : True}

class BandDetail(ReportBand):
    height = 0.6*cm
    elements = (
                ObjectValue(attribute_name='description', left = 0.5*cm, bottom = 0.1*cm,
                            top = 0.2*cm),
                ObjectValue(attribute_name='severity', left = 11*cm, botton = 0.1*cm,
                            top = 0.2*cm),
                ObjectValue(attribute_name='chance', left = 13*cm, bottom = 0.1*cm, 
                            top = 0.2*cm),
                ObjectValue(attribute_name='total_risk', left = 16*cm, bottom = 0.1*cm, 
                            top = 0.2*cm,
                            style = {'fontSize' : 13 })
                )

class BandSummary(ReportBand):
    graphs = VulnGraph()
    vulns = Vulnerability.query().all()
    graph_total_risk = graphs.do_total_vuln_graph(vulns)
    
    height = 1*cm
    elements = [
                Label(text = _('Number of Vulnerabilities:'), top = 0.3*cm, left = 0.5*cm, 
                      width = 10*cm,
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),
                ObjectValue(attribute_name = 'description', top = 0.3*cm, left = 7*cm, 
                      action = FIELD_ACTION_COUNT,
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),
                
                Label(text = _('Maximum Risk:'), top = 0.8*cm, left = 0.5*cm, 
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),                      
                ObjectValue(attribute_name = 'total_risk', top = 0.8*cm, left = 7*cm, 
                      action = FIELD_ACTION_MAX,
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),

                Label(text = _('Minimum Risk:'), top = 1.3*cm, left = 0.5*cm, 
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),                      
                ObjectValue(attribute_name = 'total_risk', top = 1.3*cm, left = 7*cm, 
                      action = FIELD_ACTION_MIN,
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),
                
                Label(text = _('Average Risk:'), top = 1.8*cm, left = 0.5*cm, 
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),
                ObjectValue(attribute_name = 'total_risk', top = 1.8*cm, left = 7*cm, 
                      action = FIELD_ACTION_AVG,
                      style = {'fontName' : 'Helvetica-Bold', 'fontSize' : 12}),
                Image(filename = graph_total_risk.name, top = 2.3*cm, left = 2*cm)
                
                ]
    borders = {'top' : True }

class BandFooter(ReportBand):
    height = 0.5*cm
    elements = [
    Label(text=_('Created by Crisk'), top=0.1*cm, left=0),
            SystemField(expression=_('Page # %(page_number)d of %(page_count)d'), top=0.1*cm,
            width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
    ]
    borders = {'top': True}


class TotalVulnReport(Report):

    page_size = A4
    margin_left = 2*cm
    margin_top = 2*cm
    margin_right = 2*cm
    margin_bottom = 2*cm

    band_page_header = BandHeader()
    band_detail = BandDetail()
    band_summary = BandSummary()
    band_page_footer = BandFooter()