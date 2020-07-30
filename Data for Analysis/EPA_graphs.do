*------------------------------------------------------------------------------*
*** All Dockets (no filter) ***

** load aggregate data **
cd "SET_DIRECTORY"
import delimited data_for_analysis_monthly, ///
varnames(1) encoding(UTF-8) bindquote(strict) clear

cd "SET_DIRECTORY"
graph set window fontface "Times New Roman"

* 1) monthly comments
graph twoway connected commentsunique receivedmonth, ///
	lcolor(navy) lwidth(medthick) ///
	xtitle("Month") title("Unique Comments",color(black) position(12) span) ///
	ytitle("Number of comments") ylabel(0(2000)10000,gstyle(major) glstyle(grid)) ///
	fcolor(white) graphregion(color(white) margin(medsmall)) ///
	saving(unique_comments_monthly, replace)

graph twoway connected commentsall receivedmonth, ///
	lcolor(navy) lwidth(medthick) ///
	xtitle("Month") title("All Comments",color(black) position(12) span) ///
	ytitle("Number of comments") ylabel(0(80000)400000,gstyle(major) glstyle(grid)) ///
	fcolor(white) graphregion(color(white) margin(medsmall)) ///
	saving(all_comments_monthly, replace)

graph combine ///
	"unique_comments_monthly" ///
	"all_comments_monthly" ///
	,rows(1) cols(2) imargin(medsmall) iscale(.7) ///
	graphr(margin(medsmall) fcolor(white) lcolor(white)) ///
	title("{bf:Figure 1: Public Comments Received by EPA, Monthly}",color(black) position(12) size(medium) span) ///
	subtitle("(January 2020 – June 2020)", color(black) position(12) size(medsmall) span) ///
	note("{bf:Notes:}  {it:Unique comments} refer to submissions posted as individual documents with a unique identifier.  {it:All comments} include " ///
	"duplicate and MCC submissions posted in groups (from API field {it:numberOfCommentsReceived})." ///
	"{bf:Source:}  Author's calculations using Regulations.gov API, retrieved July 13, 2020, https://regulationsgov.github.io/developers/.",size(small) position(7) span) ///
	saving(combo_comments_monthly, replace)
graph export "1_combo_comments_monthly.png", as(png) replace

* 2) monthly comments per dockets
graph twoway connected unq_per_dkts receivedmonth, ///
	lcolor(navy) lwidth(medthick) ///
	xtitle("Month") title("Unique Comments per Docket",color(black) position(12) span) ///
	ytitle("Ratio of comments to dockets") ylabel(,gstyle(major) glstyle(grid)) ///
	fcolor(white) graphregion(color(white) margin(medsmall)) ///
	saving(unique_adjusted_monthly, replace)

graph twoway connected all_per_dkts receivedmonth, ///
	lcolor(navy) lwidth(medthick) ///
	xtitle("Month") title("All Comments per Docket",color(black) position(12) span) ///
	ytitle("Ratio of comments to dockets") ylabel(,gstyle(major) glstyle(grid)) ///
	fcolor(white) graphregion(color(white) margin(medsmall)) ///
	saving(all_adjusted_monthly, replace)

graph combine ///
	"unique_adjusted_monthly" ///
	"all_adjusted_monthly" ///
	,rows(1) cols(2) imargin(medsmall) iscale(.7) ///
	graphr(margin(medsmall) fcolor(white) lcolor(white)) ///
	title("{bf:Figure 2: Public Comments per EPA Docket, Monthly}",color(black) position(12) size(medium) span) ///
	subtitle("(January 2020 – June 2020)", color(black) position(12) size(medsmall) span) ///
	note("{bf:Notes:}  {it:Unique comments} refer to submissions posted as individual documents with a unique identifier.  {it:All comments} include " ///
	"duplicate and MCC submissions posted in groups (from API field {it:numberOfCommentsReceived})." ///
	"{bf:Source:}  Author's calculations using Regulations.gov API, retrieved July 13, 2020, https://regulationsgov.github.io/developers/.",size(small) position(7) span) ///
	saving(combo_adjusted_monthly, replace)
graph export "2_combo_adjusted_monthly.png", as(png) replace


*------------------------------------------------------------------------------*
*** Filter Science Rule ***

** load monthly data **
cd "SET_DIRECTORY"
import delimited data_for_analysis_monthly_filterSR, ///
varnames(1) encoding(UTF-8) bindquote(strict) clear
sort receivedmonth sciencerule, stable

cd "SET_DIRECTORY"
graph set window fontface "Times New Roman"

* A1) monthly comments (exclude science rule)
graph twoway connected commentsunique receivedmonth if sciencerule==0, ///
	lcolor(navy) lwidth(medthick) ///
	xtitle("Month") title("Unique Comments",color(black) position(12) span) ///
	ytitle("Number of comments") ylabel(0(250)1500,gstyle(major) glstyle(grid)) ///
	fcolor(white) graphregion(color(white) margin(medsmall)) ///
	saving(unique_comments_monthly_excludeSR, replace)

graph twoway connected commentsall receivedmonth if sciencerule==0, ///
	lcolor(navy) lwidth(medthick) ///
	xtitle("Month") title("All Comments",color(black) position(12) span) ///
	ytitle("Number of comments") ylabel(0(25000)150000,gstyle(major) glstyle(grid)) ///
	fcolor(white) graphregion(color(white) margin(medsmall)) ///
	saving(all_comments_monthly_excludeSR, replace)

graph combine ///
	"unique_comments_monthly_excludeSR" ///
	"all_comments_monthly_excludeSR" ///
	,rows(1) cols(2) imargin(medsmall) iscale(.7) ///
	graphr(margin(medsmall) fcolor(white) lcolor(white)) ///
	title("{bf:Public Comments excluding Science Rule, Monthly}",color(black) position(12) size(medium) span) ///
	subtitle("(January 2020 – June 2020)", color(black) position(12) size(medsmall) span) ///
	note("{bf:Notes:}  Public submissions to EPA rulemaking dockets excluding {it:Strengthening Transparency in Regulatory Science}." ///
	"{it:Unique comments} refer to submissions posted as individual documents with a unique identifier.  {it:All comments} include " ///
	"duplicate and MCC submissions posted in groups (from API field {it:numberOfCommentsReceived})." ///
	"{bf:Source:}  Author's calculations using Regulations.gov API, retrieved July 13, 2020, https://regulationsgov.github.io/developers/.",size(small) position(7) span) ///
	saving(combo_comments_monthly_excludeSR, replace)
graph export "A1_combo_comments_monthly_excludeSR.png", as(png) replace

* 3) monthly comments per dockets (exclude science rule)
graph twoway connected unq_per_dkts receivedmonth if sciencerule==0, ///
	lcolor(navy) lwidth(medthick) ///
	xtitle("Month") title("Unique Comments per EPA Docket",color(black) position(12) span) ///
	ytitle("Ratio of comments to dockets") ylabel(0(5)21,gstyle(major) glstyle(grid)) ///
	fcolor(white) graphregion(color(white) margin(medsmall)) ///
	saving(unique_adjusted_monthly_excludeSR, replace)

graph twoway connected all_per_dkts receivedmonth if sciencerule==0, ///
	lcolor(navy) lwidth(medthick) ///
	xtitle("Month") title("All Comments per EPA Docket",color(black) position(12) span) ///
	ytitle("Ratio of comments to dockets") ylabel(0(500)2100,gstyle(major) glstyle(grid)) ///
	fcolor(white) graphregion(color(white) margin(medsmall)) ///
	saving(all_adjusted_monthly_excludeSR, replace)

graph combine ///
	"unique_adjusted_monthly_excludeSR" ///
	"all_adjusted_monthly_excludeSR" ///
	,rows(1) cols(2) imargin(medsmall) iscale(.7) ///
	graphr(margin(medsmall) fcolor(white) lcolor(white)) ///
	title("{bf:Figure 3: Public Comments per EPA Docket excluding Science Rule, Monthly}",color(black) position(12) size(medium) span) ///
	subtitle("(January 2020 – June 2020)", color(black) position(12) size(medsmall) span) ///
	note("{bf:Notes:}  Public submissions to EPA rulemaking dockets excluding {it:Strengthening Transparency in Regulatory Science}." ///
	"{it:Unique comments} refer to submissions posted as individual documents with a unique identifier.  {it:All comments} include " ///
	"duplicate and MCC submissions posted in groups (from API field {it:numberOfCommentsReceived})." ///
	"{bf:Source:}  Author's calculations using Regulations.gov API, retrieved July 13, 2020, https://regulationsgov.github.io/developers/.",size(small) position(7) span) ///
	saving(combo_adjusted_monthly_excludeSR, replace)
graph export "3_combo_adjusted_monthly_excludeSR.png", as(png) replace

** load daily data **
cd "SET_DIRECTORY"
import delimited data_for_analysis_daily_filterSR, ///
varnames(1) encoding(UTF-8) bindquote(strict) clear
sort dtreceived sciencerule, stable

* https://www.ssc.wisc.edu/sscc/pubs/stata_dates.htm
gen date_received = date(dtreceived,"YMD")
format date_received %td

gen covid = 1 if date_received >= td(11mar2020)
replace covid = 0 if date_received < td(11mar2020)

cd "SET_DIRECTORY"
graph set window fontface "Times New Roman"

* 4) daily comments (exclude science rule)
graph twoway line commentsunique date_received if sciencerule==0, ///
	tline(11mar2020, lpattern(dash)) ///
	ttext(380 23feb2020 "",color(black)) ///
	lcolor(navy) lwidth(medium) ///	
	xtitle("Date",color(black)) ///
	title("Unique Comments",color(black) position(12) span) ///
	ytitle("Number of comments",color(black)) ylabel(,gstyle(major) glstyle(grid)) ///
	xlabel(#5) xtick(#6) ///
	fcolor(white) graphregion(color(white) margin(large)) ///
	saving(unique_comments_daily_excludeSR, replace)
	
graph twoway line commentsall date_received if sciencerule==0, ///
	tline(11mar2020, lpattern(dash)) ///
	ttext(50000 1apr2020 "",color(black)) ///
	lcolor(navy) lwidth(medium) ///
	xtitle("Date",color(black)) ///
	title("All Comments",color(black) position(12) span) ///
	ytitle("Number of comments",color(black)) ylabel(,gstyle(major) glstyle(grid)) ///
	xlabel(#5) xtick(#6) ///
	fcolor(white) graphregion(color(white) margin(large)) ///
	saving(all_comments_daily_excludeSR, replace)

graph combine ///
	"unique_comments_daily_excludeSR" ///
	"all_comments_daily_excludeSR" ///
	,rows(2) cols(1) imargin(medsmall) iscale(.7) ///
	graphr(margin(medsmall) fcolor(white) lcolor(white)) ///
	title("{bf:Figure 4: Public Comments excluding Science Rule, Daily}",color(black) position(12) size(medium) span) ///
	subtitle("(January 1, 2020 – June 30, 2020)", color(black) position(12) size(medsmall) span) ///
	note("{bf:Notes:}  Public submissions to EPA rulemaking dockets, excluding {it:Strengthening Transparency in Regulatory Science}." ///
	"Dashed line at March 11 marks the World Health Organization characterizing COVID-19 as a pandemic. {it:Unique comments} " ///
	"refer to submissions posted as individual documents with a unique identifier.  {it:All comments} include duplicate and MCC " ///
	"submissions posted in groups (from API field {it:numberOfCommentsReceived})." ///
	"{bf:Source:}  Author's calculations using Regulations.gov API, retrieved July 13, 2020, https://regulationsgov.github.io/developers/.",size(small) position(7) span) ///
	saving(combo_comments_daily_excludeSR, replace)
graph export "4_combo_comments_daily_excludeSR.png", as(png) replace

* A2) daily comments per dockets (exclude science rule)
graph twoway line unq_per_dkts date_received if sciencerule==0, ///
	tline(11mar2020, lpattern(dash)) ///
	lcolor(navy) lwidth(medium) ///	
	xtitle("Date",color(black)) ///
	title("Unique Comments per Docket",color(black) position(12)) ///
	ytitle("Ratio of comments to dockets",color(black)) ylabel(,gstyle(major) glstyle(grid)) ///
	xlabel(#5) xtick(#6) ///
	fcolor(white) graphregion(color(white) margin(large)) ///
	saving(unique_adjusted_daily_excludeSR, replace)

graph twoway line commentsall date_received if sciencerule==0, ///
	tline(11mar2020, lpattern(dash)) ///
	lcolor(navy) lwidth(medium) ///
	xtitle("Date",color(black)) ///
	title("All Comments per Docket",color(black) position(12)) ///
	ytitle("Ratio of comments to dockets",color(black)) ylabel(,gstyle(major) glstyle(grid)) ///
	xlabel(#5) xtick(#6) ///
	fcolor(white) graphregion(color(white) margin(large)) ///
	saving(all_adjusted_daily_excludeSR, replace)

graph combine ///
	"unique_adjusted_daily_excludeSR" ///
	"all_adjusted_daily_excludeSR" ///
	,rows(2) cols(1) imargin(medsmall) iscale(.7) ///
	graphr(margin(medsmall) fcolor(white) lcolor(white)) ///
	title("{bf: Public Comments per Docket excluding Science Rule, Daily}",color(black) position(12) size(medium) span) ///
	subtitle("(January 1, 2020 – June 30, 2020)", color(black) position(12) size(medsmall) span) ///
	note("{bf:Notes:}  Public submissions to EPA rulemaking dockets, excluding {it:Strengthening Transparency in Regulatory Science}." ///
	"Dashed line at March 11 marks the World Health Organization characterizing COVID-19 as a pandemic. {it:Unique comments} " ///
	"refer to submissions posted as individual documents with a unique identifier.  {it:All comments} include duplicate and MCC " ///
	"submissions posted in groups (from API field {it:numberOfCommentsReceived})." ///
	"{bf:Source:}  Author's calculations using Regulations.gov API, retrieved July 13, 2020, https://regulationsgov.github.io/developers/.",size(small) position(7) span) ///
	saving(combo_adjusted_daily_excludeSR, replace)
graph export "A2_combo_adjusted_daily_excludeSR.png", as(png) replace

