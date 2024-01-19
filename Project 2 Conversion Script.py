# Features
# Cumulative Delta
# Open
# Close
# Volume
#      BuyVolume
#      Sell Volume
# MA 20
# MA 50
# VWAP
# STD1
# STD2
# STD3


// Input variables for candle colors
candleBullColor = input.color(color.green, title='Bullish Candle Color', group='Candle Colors')
candleBearColor = input.color(color.red, title='Bearish Candle Color', group='Candle Colors')

// Input variables for divergence colors
bullishDivergenceColor = input.color(color.rgb(255, 209, 58), title='Bullish Divergence Color', group='Divergence Colors')
bearishDivergenceColor = input.color(color.rgb(73, 173, 255), title='Bearish Divergence Color', group='Divergence Colors')

var float buyVolume = 0.0
var float sellVolume = 0.0
var float delta = 0.0

// Calculate Delta
buyVolume := math.sum(volume * (close >= open ? 1 : 0), 1)
sellVolume := math.sum(volume * (close < open ? 1 : 0), 1)
delta := buyVolume - sellVolume

// Moving Averages of Cumulative Delta
cumulativeDelta = ta.cum(delta)
maLength1 = input(20, title="Moving Average Length 1")
maLength2 = input(50, title="Moving Average Length 2")
maCumulativeDelta1 = ta.sma(cumulativeDelta, maLength1)
maCumulativeDelta2 = ta.sma(cumulativeDelta, maLength2)

// Color candles based on delta
barColor = delta >= 0 ? candleBullColor : candleBearColor

// Convert Cumulative Delta to candles
cdOpen = cumulativeDelta[1]
cdClose = cumulativeDelta
cdHigh = math.max(cdOpen, cdClose)
cdLow = math.min(cdOpen, cdClose)

// Detect Divergences
bullishDivergence = close > open and delta < delta[1]
bearishDivergence = close < open and delta > delta[1]

// Color the delta candles based on divergences
deltaColor = delta >= 0 ? (bullishDivergence ? bullishDivergenceColor : candleBullColor) : (bearishDivergence ? bearishDivergenceColor : candleBearColor)

// Plot Cumulative Delta candles
plotcandle(cdOpen, cdHigh, cdLow, cdClose, title='Cumulative Delta Candles', color=deltaColor, wickcolor=deltaColor)

// Plot Moving Averages of Cumulative Delta as line charts
plot(maCumulativeDelta1, color=color.rgb(21, 255, 0), title="MA Cumulative Delta 1")
plot(maCumulativeDelta2, color=color.rgb(255, 0, 81), title="MA Cumulative Delta 2")

// 
hideonDWM = input(false, title="Hide VWAP on 1D or Above", group="VWAP Settings")
var anchor = input.string(defval = "Session", title="Anchor Period",
 options=["Session", "Week", "Month", "Quarter", "Year", "Decade", "Century", "Earnings", "Dividends", "Splits"], group="VWAP Settings")
src = input(title = "Source", defval = hlc3, group="VWAP Settings")
offset = input.int(0, title="Offset", group="VWAP Settings", minval=0)

BANDS_GROUP = "Bands Settings"
CALC_MODE_TOOLTIP = "Determines the units used to calculate the distance of the bands. When 'Percentage' is selected, a multiplier of 1 means 1%."
calcModeInput = input.string("Standard Deviation", "Bands Calculation Mode", options = ["Standard Deviation", "Percentage"], group = BANDS_GROUP, tooltip = CALC_MODE_TOOLTIP)
showBand_1 = input(true, title = "", group = BANDS_GROUP, inline = "band_1")
bandMult_1 = input.float(1.0, title = "Bands Multiplier #1", group = BANDS_GROUP, inline = "band_1", step = 0.5, minval=0)
showBand_2 = input(false, title = "", group = BANDS_GROUP, inline = "band_2")
bandMult_2 = input.float(2.0, title = "Bands Multiplier #2", group = BANDS_GROUP, inline = "band_2", step = 0.5, minval=0)
showBand_3 = input(false, title = "", group = BANDS_GROUP, inline = "band_3")
bandMult_3 = input.float(3.0, title = "Bands Multiplier #3", group = BANDS_GROUP, inline = "band_3", step = 0.5, minval=0)

if barstate.islast and ta.cum(volume) == 0
    runtime.error("No volume is provided by the data vendor.")

new_earnings = request.earnings(syminfo.tickerid, earnings.actual, barmerge.gaps_on, barmerge.lookahead_on, ignore_invalid_symbol=true)
new_dividends = request.dividends(syminfo.tickerid, dividends.gross, barmerge.gaps_on, barmerge.lookahead_on, ignore_invalid_symbol=true)
new_split = request.splits(syminfo.tickerid, splits.denominator, barmerge.gaps_on, barmerge.lookahead_on, ignore_invalid_symbol=true)

isNewPeriod = switch anchor
	"Earnings"  => not na(new_earnings)
	"Dividends" => not na(new_dividends)
	"Splits"    => not na(new_split)
	"Session"   => timeframe.change("D")
	"Week"      => timeframe.change("W")
	"Month"     => timeframe.change("M")
	"Quarter"   => timeframe.change("3M")
	"Year"      => timeframe.change("12M")
	"Decade"    => timeframe.change("12M") and year % 10 == 0
	"Century"   => timeframe.change("12M") and year % 100 == 0
	=> false

isEsdAnchor = anchor == "Earnings" or anchor == "Dividends" or anchor == "Splits"
if na(src[1]) and not isEsdAnchor
	isNewPeriod := true



float vwapValue = na
float upperBandValue1 = na
float lowerBandValue1 = na
float upperBandValue2 = na
float lowerBandValue2 = na
float upperBandValue3 = na
float lowerBandValue3 = na

if not (hideonDWM and timeframe.isdwm)
    [_vwap, _stdevUpper, _] = ta.vwap(src, isNewPeriod, 1)
	vwapValue := _vwap
    stdevAbs = _stdevUpper - _vwap
	bandBasis = calcModeInput == "Standard Deviation" ? stdevAbs : _vwap * 0.01
	upperBandValue1 := _vwap + bandBasis * bandMult_1
	lowerBandValue1 := _vwap - bandBasis * bandMult_1
	upperBandValue2 := _vwap + bandBasis * bandMult_2
	lowerBandValue2 := _vwap - bandBasis * bandMult_2
	upperBandValue3 := _vwap + bandBasis * bandMult_3
	lowerBandValue3 := _vwap - bandBasis * bandMult_3

plot(vwapValue, title="VWAP", color=#2962FF, offset=offset)

upperBand_1 = plot(upperBandValue1, title="Upper Band #1", color=color.green, offset=offset, display = showBand_1 ? display.all : display.none)
lowerBand_1 = plot(lowerBandValue1, title="Lower Band #1", color=color.green, offset=offset, display = showBand_1 ? display.all : display.none)
fill(upperBand_1, lowerBand_1, title="Bands Fill #1", color= color.new(color.green, 95)    , display = showBand_1 ? display.all : display.none)

upperBand_2 = plot(upperBandValue2, title="Upper Band #2", color=color.olive, offset=offset, display = showBand_2 ? display.all : display.none)
lowerBand_2 = plot(lowerBandValue2, title="Lower Band #2", color=color.olive, offset=offset, display = showBand_2 ? display.all : display.none)
fill(upperBand_2, lowerBand_2, title="Bands Fill #2", color= color.new(color.olive, 95)    , display = showBand_2 ? display.all : display.none)

upperBand_3 = plot(upperBandValue3, title="Upper Band #3", color=color.teal, offset=offset, display = showBand_3 ? display.all : display.none)
lowerBand_3 = plot(lowerBandValue3, title="Lower Band #3", color=color.teal, offset=offset, display = showBand_3 ? display.all : display.none)
fill(upperBand_3, lowerBand_3, title="Bands Fill #3", color= color.new(color.teal, 95)    , display = showBand_3 ? display.all : display.none)

plot(upperBandValue1, "upper STD1", color=color.green)
plot(lowerBandValue1, "lower STD1", color=color.green)
plot(upperBandValue2, "upper STD2", color=color.olive)
plot(lowerBandValue2, "lower STD2", color=color.olive)
plot(upperBandValue3, "upper STD3", color=color.teal)
plot(lowerBandValue3, "lower STD3", color=color.teal)

// Conditions
vwapShort1 = close > upperBandValue1
vwapshort2 = close > upperBandValue2
vwapshort3 = close > upperBandValue3

vwapLong1 = close < lowerBandValue1
vwapLong2 = close < lowerBandValue2
vwapLong3 = close < lowerBandValue3

// Stop Loss/ Take profit


profitTarget = strategy.openprofit * 1.15 // 15% profit target
trailStopLoss = strategy.position_avg_price * 0.95 // 5% stop loss

// Define your trailing stop offset as a percentage
trail_offset_percentage = input.float(2, title="Trailing Stop Offset (%)") / 100

// Calculate the trailing stop level as a percentage of the close price
trail_stop_level = close * (1 - trail_offset_percentage)




/////// Entry/ Exit Conditions
// if (bearishDivergence and vwapShort1)
//     strategy.entry("1st deviation short signal", strategy.short, qty = 3)
// 	strategy.exit(id = "1st deviation close short signal", from_entry = "1st deviation short signal", profit = profitTarget, trail_offset = trail_stop_level)
	//strategy.exit(id = "1st deviation close short signal", from_entry = "1st deviation short signal", profit = profitTargetL)

// if (bullishDivergence and vwapLong1)
//     strategy.entry("1st deviation long signal", strategy.long, qty = 3)
// 	strategy.exit(id = "1st deviation close long signal", from_entry = "1st deviation long signal", trail_points = trailStopLoss, trail_offset = 0)
	//strategy.exit(id = "1st deviation close short signal", from_entry = "1st deviation long signal", profit = profitTargetL)

if (bearishDivergence and vwapshort2)
    strategy.entry("2nd deviation short signal", strategy.short, qty = 3)
	strategy.exit(id = "2nd deviation close short signal", from_entry = "2nd deviation short signal", trail_points = trailStopLoss, trail_offset = 0)
	//strategy.exit(id = "2nd deviation close short signal", from_entry = "2nd deviation short signal", profit = profitTargetL)

if (bullishDivergence and vwapLong2)
    strategy.entry("2nd devition long signal", strategy.long, qty = 3)
	strategy.exit(id = "2nd deviation close long signal", from_entry = "2nd deviation long signal", trail_points = trailStopLoss, trail_offset = 0)
	//strategy.exit(id = "2nd deviation close short signal", from_entry = "2nd deviation long signal", profit = profitTargetL)

if (bearishDivergence and vwapshort3)
    strategy.entry("3rd deviation short signal", strategy.short, qty = 3)
	strategy.exit(id = "3rd deviation close short signal", from_entry = "3rd deviation short signal", trail_points = trailStopLoss, trail_offset = 0)
	//strategy.exit(id = "3rd deviation close short signal", from_entry = "3rd deviation short signal", profit = profitTargetL)

if (bullishDivergence and vwapLong3)
    strategy.entry("3rd deviation long signal", strategy.long, qty = 3)
	strategy.exit(id = "3rd deviation close long signal", from_entry = "3rd deviation long signal", trail_points = trailStopLoss, trail_offset = 0)
	//strategy.exit(id = "3rd deviation close long signal", from_entry = "3rd deviation long signal", profit = profitTargetL)
// Setting a 5% trailing stop loss





