# ----------------------------------------------------------------------
# Information
# ----------------------------------------------------------------------

# Structural topic model
#
# (Author) Hans-Peter Höllwirth
# (Date)   06.2017


# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# house cleaning
rm(list = ls())
par(mfrow=c(1,1))
save.plot <- FALSE

# load libraries
library(stm)

# if interactive, during the development, set to TRUE
interactive <- FALSE
if (interactive) {
    setwd("/Users/Hans-Peter/Documents/Masters/14D010/project/code")
} 


# ----------------------------------------------------------------------
# Load and prepare data
# ----------------------------------------------------------------------
data <- read.csv('../data/combined.csv')

# one-hot encoding of president
presidents <- unique(data[,'President'])
one.hot.encode <- matrix(nrow=nrow(data), ncol=length(presidents))
for (p in 1:length(presidents)) {
    one.hot.encode[,p] <- as.numeric((data[,'President'] == presidents[p]))
}
meta.data <- data.frame(one.hot.encode)
colnames(meta.data) <- presidents

# ----------------------------------------------------------------------
# Train Structural Topic Model with K=3
# ----------------------------------------------------------------------
topic.stopwords <- c('activ', 'alreadi', 'also', 'analysi', 'annual', 'area', 'assess', 'bank', 'base', 'basi', 'chang', 'close', 'come', 'concern', 'condit', 'confid', 'confirm', 'continu', 'contribut', 'could', 'council', 'countri', 'cours', 'current', 'data', 'decid', 'decis', 'develop', 'dispos', 'ecb', 'econom', 'economi', 'effect', 'euro', 'european', 'expect', 'explain', 'financi', 'first', 'fiscal', 'follow', 'futur', 'gentlemen', 'govern', 'growth', 'hicp', 'high', 'howev', 'import', 'includ', 'increas', 'indic', 'inflat', 'inform', 'interest', 'ladi', 'last', 'let', 'level', 'like', 'line', 'look', 'made', 'maintain', 'make', 'market', 'medium', 'meet', 'monetari', 'month', 'much', 'need', 'one', 'order', 'outcom', 'outlook', 'particular', 'past', 'period', 'point', 'polici', 'posit', 'present', 'press', 'price', 'privat', 'public', 'question', 'rate', 'real', 'recent', 'reflect', 'reform', 'regard', 'relat', 'remain', 'report', 'risk', 'said', 'say', 'second', 'sector', 'see', 'sinc', 'stabil', 'start', 'still', 'structur', 'support', 'take', 'term', 'think', 'time', 'today', 'turn', 'two', 'vicepresid', 'well', 'would', 'year')
corpus <- textProcessor(data[,'Text'], metadata=meta.data, customstopwords=topic.stopwords)
stm.input <- prepDocuments(corpus$documents, corpus$vocab, corpus$meta) # test lower.tresh

set.seed(3013)
stm.output <- stm(stm.input$documents, stm.input$vocab, K=3, verbose=FALSE,
                  prevalence=~Duisenberg+Trichet+Draghi, data=stm.input$meta)  

# ----------------------------------------------------------------------
# Understand effect of presidents on topic distribution
# ----------------------------------------------------------------------

# estimate effect of presidents on topic distribution
set.seed(3013)
effect <- estimateEffect(1:3 ~ Duisenberg+Trichet+Draghi, stm.output, metadata=stm.input$meta, nsims=10)
effect.para <- data.frame(matrix(nrow=3, ncol=4), row.names = c('Topic 1','Topic 2','Topic 3'))
colnames(effect.para) <- c('Intercept','Duisenberg','Trichet','Draghi')
for (t in 1:3) {
    parameters <- matrix(nrow=10, ncol=4)
    for (i in 1:10) {
         parameters[i,] <- effect$parameters[[t]][[i]]$est
    }
    effect.para[t,] <- c(median(parameters[,1]), median(parameters[,2]), median(parameters[,3]), median(parameters[,4]))
}
round(effect.para,3)

# ----------------------------------------------------------------------
# Train Structural Topic Model with K=10
# ----------------------------------------------------------------------
corpus <- textProcessor(data[,'Text'], metadata=meta.data)
stm.input <- prepDocuments(corpus$documents, corpus$vocab, corpus$meta, upper.thresh=185) 

K <- 10
set.seed(3010)
stm.output <- stm(stm.input$documents, stm.input$vocab, K=K, verbose=FALSE,
                  prevalence=~Duisenberg+Trichet+Draghi, data=stm.input$meta) 

# ----------------------------------------------------------------------
# Plot and Output Topic Distributions
# ----------------------------------------------------------------------
col.scheme.10 <- c('skyblue3', 'orange', 'sienna', 'green', 'deeppink', 'magenta', 'blue', 'cyan', 'red', 'yellow')

# topic distribution plot
if(save.plot) png(paste0('../images/topicDistr_K10.png'), width=700, height=350, pointsize=16)
layout(cbind(1,2), widths=c(8,1))
par( mar=c(2.5,4.4,0.5,0.1) )
plot(as.Date(data[,'Date']), rep(0,222), type='l', lwd=3, ylim=c(0,1), ylab='topic distribution', xaxt ='n', yaxt='n', las=2)
for (i in 1:10) {
    lines(as.Date(data[,'Date']), ifelse(stm.output$theta[,i]<0.2,0,stm.output$theta[,i]), col=col.scheme.10[i], lwd=2)
}
xticks <- axis.Date(1, at=seq(as.Date("1998/1/1"), as.Date("2017/1/1"), "years"), cex.axis=0.8, srt=45)
yticks <- axis(2 , las=1, at=seq(0,1,0.2), cex.axis=0.8)
abline( v=xticks , col = 'grey' )
abline( h=yticks , col = 'grey' )
par(mar=c(0, 0, 0, 0))
plot.new()
legend("right","center", seq(1,10), col=col.scheme.10, lty=1, lwd=2.5, bty ="n", seg.len=1, x.intersp=0.5)
if(save.plot) dev.off()
layout(cbind(1,1))


# function plots topic share for given topic
plot.topic.distr <- function(topic, save.plot=FALSE) {
    if(save.plot) png(paste0('../images/topicShare_K10_',topic,'.png'), width=500, height=300, pointsize=16)
    par( mar=c(2.5,4.4,3,0.1) )
    plot(as.Date(data[,'Date']), stm.output$theta[,topic], type='l', col=col.scheme.10[topic %% 2 + 1], lwd=3, main=paste('Topic',topic), ylim=c(0,1), ylab='topic share', xaxt ='n', yaxt='n', las=2)
    xticks <- axis.Date(1, at=seq(as.Date("1998/1/1"), as.Date("2017/1/1"), "years"), cex.axis=0.8, srt=45)
    yticks <- axis(2 , las=1, at=seq(0,1,0.2), cex.axis=0.8)
    abline( v=xticks , col = 'grey' )
    abline( h=yticks , col = 'grey' )
    if(save.plot) dev.off()
}

# function returns data frame of n top words (with different methods) for given topic
get.top.words <- function(topic, n=7) {
    top.words <- data.frame(matrix(nrow=4, ncol=n), row.names = c('HProb','FREX','Lift','Score'))
    colnames(top.words) <- seq(1,n)
    
    words <- labelTopics(stm.output, n=n)
    top.words['HProb',] <- words$prob[topic,]
    top.words['FREX',]  <- words$frex[topic,]
    top.words['Lift',]  <- words$lift[topic,]
    top.words['Score',] <- words$score[topic,]
    
    return(top.words)
}

# plot topic share for topics 1-10
plot.topic.distr(1, save.plot=FALSE)
plot.topic.distr(2, save.plot=FALSE)
plot.topic.distr(3, save.plot=FALSE)
plot.topic.distr(4, save.plot=FALSE)
plot.topic.distr(5, save.plot=FALSE)
plot.topic.distr(6, save.plot=FALSE)
plot.topic.distr(7, save.plot=FALSE)
plot.topic.distr(8, save.plot=FALSE)
plot.topic.distr(9, save.plot=FALSE)
plot.topic.distr(10, save.plot=FALSE)

get.top.words(1)
get.top.words(2)
get.top.words(3)
get.top.words(4)
get.top.words(5)
get.top.words(6)
get.top.words(7)
get.top.words(8)
get.top.words(9)
get.top.words(10)

# ----------------------------------------------------------------------
# Understand effect of presidents on topic distribution
# ----------------------------------------------------------------------

# estimate effect of presidents on topic distribution
set.seed(3013)
effect <- estimateEffect(1:10 ~ Duisenberg+Trichet+Draghi, stm.output, metadata=stm.input$meta, nsims=10)
effect.para <- data.frame(matrix(nrow=10, ncol=4), row.names = seq(1,10))
colnames(effect.para) <- c('Intercept','Duisenberg','Trichet','Draghi')
for (t in 1:10) {
    parameters <- matrix(nrow=10, ncol=4)
    for (i in 1:10) {
        parameters[i,] <- effect$parameters[[t]][[i]]$est
    }
    effect.para[t,] <- c(median(parameters[,1]), median(parameters[,2]), median(parameters[,3]), median(parameters[,4]))
}
round(effect.para,3)

# ----------------------------------------------------------------------
# Topic correlation
# ----------------------------------------------------------------------
topic.corr <- topicCorr(stm.output)
round(ifelse(abs(topic.corr$cor) < 0.2, NA, topic.corr$cor),2)
plot(topic.corr)


