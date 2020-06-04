# 465 Project

# Ideas 
# League batting average progressions
# Player hot spots and vs pitches (heatmap)
# Pitchers tendencies (scatter and bar)
# Pitcher vs Batter stats (heatmap and maybe some distribution thing?)

# Do a pitches by location scatter plot Each pitch is a shape and each result is a color
# compare each month's map to each other. This can show that certain pitches are more
# effective at different parts of the year including weather conditions.

# Make all of this into an interactive dash sheet. With an sqlite3 database behind
# it so that you do not have to reference csvs all the time.

# https://www.kaggle.com/pschale/mlb-pitch-data-20152018


atbats <- read_csv("Desktop/DePaul/DSC_465/Project/mlb-pitch-data-20152018/atbats.csv")
player_names <- read_csv("Desktop/DePaul/DSC_465/Project/mlb-pitch-data-20152018/player_names.csv")
pitches <- read_csv("Desktop/DePaul/DSC_465/Project/mlb-pitch-data-20152018/pitches.csv")

pitches_100 <- pitches[1:500000,]

# Notes
# pz and px are in feet. +/- 8.5 inches for the plate 0.70 for the plate
# Type test us ball B, strike S or ball in play X
# pitch_type shows type of pitch that was thrown

#CH - Changeup
#CU - Curveball
#EP - Eephus*
#FC - Cutter
#FF - Four-seam Fastball
#FO - Pitchout (also PO)*
#FS - Splitter
#FT - Two-seam Fastball
#IN - Intentional ball
#KC - Knuckle curve
#KN - Knuckeball
#PO - Pitchout (also FO)*
#SC - Screwball*
#SI - Sinker
#SL - Slider

plot(pitches_100$px, pitches_100$pz, type='n')
text(pitches_100$px, pitches_100$pz, labels = as.character(pitches_100$zone))

# My questimated strike zone. The width is correct the height is right for the average size player.
abline(v = 0.7)
abline(v = -0.7)
abline(h = 1.5)
abline(h = 4)
# So I will divide this into 9 evenly sized quadrants
abline(v = -.23)
abline(v = .23)
abline(h = 2.33)
abline(h = 3.16)

# Next steps
# Find one batter and create their heatmap as it were for 2015 only.
# This is only on last pitch of at bat. Use the code to determine that.
# determine what zone each result is a version of. That might be the zone key (looks like 1-9 from top left to bot right, 11 up and away 13 down away, 12 up-in 14 down-in)
# Going to be easier to just use that potentially. and just draw it prettier.
# determine what is hot and what is cold and neutral.

# This is a hybrid cartogram so I am going to use it for question 1 for HW4

# Then I think I am going to do some pitcher data.
# I could do a basic time series of a pitchers velocity per inning on fastballs for starters???

# Code
#B - Ball
#*B - Ball in dirt
#S - Swinging Strike
#C - Called Strike
#F - Foul
#T - Foul Tip
#L - Foul Bunt
#I - Intentional Ball
#W - Swinging Strike (Blocked)
#M - Missed Bunt
#P - Pitchout
#Q - Swinging pitchout
#R - Foul pitchout
#Values that only occur on last pitch of at-bat:
#X - In play, out(s)
#D - In play, no out
#E - In play, runs
#H - Hit by pitch


library(tidyverse)
tmp <- pitches_100 %>%
  filter(code %in% c('X', 'D', 'E', 'H')) %>%
  inner_join(atbats, by='ab_id')
tmp

tmp$event

plot(tmp$px, tmp$pz, type='n')
text(tmp$px, tmp$pz, labels = as.character(tmp$zone))

# Done this returns all of the results from the at_bats for each final pitch.
tmp2 <- pitches_100 %>%
  group_by(ab_id) %>%
  filter(pitch_num == max(pitch_num)) %>%
  inner_join(atbats, by='ab_id')
  

tmp2 <- tmp2 %>%
  ungroup() %>%
  group_by(batter_id)

tmp3 <- group_split(tmp2)

tmp3[1][[1]]$batter_id

player_names %>%
  filter(id == 112526)

plot(tmp3[1][[1]]$px, tmp3[1][[1]]$pz, xlim=c(-3, 3), ylim=c(-1, 5), col = as.factor(tmp3[1][[1]]$event))
text(tmp3[1][[1]]$px, tmp3[1][[1]]$pz, labels = as.character(tmp3[1][[1]]$event))

library(ggplot2)
as.data.frame(tmp3[1][[1]])

as.data.frame(tmp3[1][[1]]) %>%
  ggplot(aes(px, pz)) + geom_point() + geom_segment(aes(x = -0.7, y = 1.5, xend = 0.7, yend = 1.5)) + geom_segment(aes(x = -0.7, y = 4, xend = 0.7, yend = 4)) + geom_segment(aes(x = -0.7, y = 1.5, xend = -0.7, yend = 4))

abline(v = 0.7)
abline(v = -0.7)
abline(h = 1.5)
abline(h = 4)
# So I will divide this into 9 evenly sized quadrants
abline(v = -.23)
abline(v = .23)
abline(h = 2.33)
abline(h = 3.16)



tmp2$event
# or pitch_num == max(pitch_num) for that at-bat?

  
