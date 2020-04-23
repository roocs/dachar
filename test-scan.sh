#!/bin/bash

#python scan.py -l ceda -d CMIP6.AerChemMIP.MOHC.UKESM1-0-LL.piClim-2xNOx.r1i1p1f2.day.vas.gn.latest -m quick cmip6

#python scan.py -l ceda -p /badc/cmip6/data/CMIP6/AerChemMIP/MOHC/UKESM1-0-LL/piClim-2xNOx/r1i1p1f2/day -m quick cmip6

#python scan.py -l ceda -d cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas -m quick cmip5

# facets="activity product institute model experiment frequency realm mip_table ensemble_member version variable"
# /badc/cmip5/data/cmip5/output1/*/*/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*

facets="activity=cmip5,product=output1,experiment=rcp45,frequency=mon,realm=ocean,mip_table=Omon,ensemble_member=r1i1p1,version=latest,variable=zostoga"
#dachar scan -l ceda -f $facets -m quick cmip5

#dachar scan -l ceda -d cmip5.output1.MRI.MRI-CGCM3.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga -m full cmip5

#dachar scan -l ceda -d c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.psl.v20190212 -m quick c3s-cordex

#python scan.py -l ceda -d c3s-cordex.output.EUR-11.CNRM.CNRM-CERFACS-CNRM-CM5.rcp45.r1i1p1.CNRM-ALADIN53.v1.day.tas.v20150127 -m quick c3s-cordex

dachar scan -l ceda -d c3s-cordex.output.EUR-11.IPSL.MOHC-HadGEM2-ES.rcp85.r1i1p1.IPSL-WRF381P.v1.day.tas.v20190212 -m quick c3s-cordex
