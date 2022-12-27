########## PRODUÇÃO DE SOJA NO BRASIL ########## 

# SOJA: https://seriesestatisticas.ibge.gov.br/series.aspx?no=1&op=0&vcodigo=PA3&t=lavoura-temporaria-quantidade-produzida
# PIB: https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html?=&t=series-historicas&utm_source=landing&utm_medium=explica&utm_campaign=pib
# http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=521274780&module=M
# https://www.youtube.com/watch?v=PPumHDWBCcA

# Pacotes Utilizados
install.packages("pacman")
library("pacman")

p_load(tidyverse, readxl, dplyr, stringr, data.table, ggplot2, ggfortify, forecast, urca, TSA, lmtest, normtest, shiny)

# Desabilitando notacao cientifica
options(scipen=999)

# Definir o diretório de trabalho#
getwd()

# Atualize para o seu diret?rio de trabalho##
setwd("C:/Users/Usuario/Documents/IESB_2022/7_semestre/series_temporais")

############ SOJA ################
# Leitura dos dados
df <- read.csv("serie_historica_soja.txt", sep="\t")
View(df)
head(df)

# Remove coluna não utilizada
df1 <- df[,-1]
View(df1)

# Realiza a trasposta dos dados
df2 <- t(df1)
View(df2)

# Reestrutura index para coluna
df3 <- cbind(ANO = rownames(df2), df2)
rownames(df3) <- 1:nrow(df3)
View(df3)

# Deleta linha não utilizada
df4 <- df3[-1,]
View(df4)

# Retira 'X' da coluna 'ANO'
df5 <- gsub("X", "", df4)
View(df5)

# Renomeia coluna
colnames(df5)[2] = "PRODUCAO"
rownames(df5) <- 1:nrow(df5)
View(df5)

# Verificando características da base de dados
head(df5)
tail(df5)
summary(df5)

# Transforma para dataframe
df6 <- as.data.frame(df5)


# Alterando o tipo do dado
is.numeric(df6$ANO)
is.numeric(df6$PRODUCAO)

df6$ANO <- as.numeric(df6$ANO)
df6$PRODUCAO <- as.numeric(df6$PRODUCAO)

head(df6)
tail(df6)

summary(df6)

write.table(df6,"producao_soja_st.txt", sep=";")
?write.table

# Transforma em série temporal
df_ts <- ts(data=df6$PRODUCAO, start=1990, freq=1)
df_ts

# Características da série temporal
start(df_ts)
end(df_ts)
class(df_ts)

## 1 - Correlograma e seus componentes

#-- dados brutos OK
#- correlograma. OK
#- observar a exsitencia de tres componente tendencia, sazonalidade e ciclo. OK (tendencia e ciclo)

plot(df_ts, xlab="ANO", ylab="QTD SOJA", main="PRODUÇÃO DE SOJA POR ANO NO BRASIL", col="blue")

#### Podemos verificar que a série temporal não possui sazonalidade, portanto:
#- **Tendência:** Os dados possuem uma tendência forte de aumento.
#- **Sazonalidade:** Os dados não possuem a componente sazonal, não obdeceno padrães com durações fixas.
#- **CIclo:** A série possui um componente variando em ciclos, porém sem duração fixa.

# Decomposição da série temporal
df_decomp <- decompose(df_ts)
df_decomp

autoplot(df_decomp)

# Não é possível realizar a decomposição da série temporal, possivelmente por seu curto perído de tempo anual, e por não ter a componente sazonal.

## 2 - Modelos de Suavização Exponencial
#Como vimos acima, a série não possui sazonalidade, portanto, não se aplicaria o modelo de suavização exponencial sazonal de Holt-Winters (HW).
#Porém, para efeito de estudo, será implementado cada um destes, a fim de verificar seu comportamente perante a série temporal.

#- Aplicando os Modelos Suavização Exponencial.

### 2.1 - Suavização Exponencial Simples (SES)
#Série livre das compoenentes de *tendência* e *sazonalidade*.
df_ts_ses <- ses(df_ts, h=6)
df_ts_ses$model

autoplot(df_ts_ses)

### 2.2 - Suavização Exponencial de Holt (SEH)
#Série que apresenta tendência, mas sem a componente de sazonalidade.
df_ts_holt <- holt(df_ts, h=6)
df_ts_holt$model

autoplot(df_ts_holt)

### 2.3 - Suavização Exponencial Sazonal de Holt-Winters (HW)
#Série apresenta sazonalidade.
#- Método Aditivo: Amplitude dos ciclos de sazonalidade não está correlacionada ao tempo.
#- Método Multiplicativo: Amplitude dos ciclos de sazonalidade está correlacionado ao tempo.

#**OBS:** Não é o caso da série estudada, mas a efeito de estudos, será observada o comportamento deste modelo.
### 2.3 - Suavização Exponencial Sazonal de Holt-Winters (HW)
#- Método Aditivo
df_ts_hwa <- hw(df_ts, seasonal="additive", h=6)
df_ts_hwa$model

autoplot(df_ts_hwa)

#- Método Multiplicativo
df_ts_hwm <- hw(df_ts, seasonal="multiplicative", h=6)
df_ts_hwm$model

autoplot(df_ts_hwm)

df_ts_ses$mean
df_ts_holt$x

## 3 - Processo Estocastico

#- H0: É um processo estocástico.
#- H1: Não é um processo estocástico.

## 4 - Processos Estacionário ou Não-Estacionário

#ACF e PACF

#- H0: A série é não estacionária.
#- H1: A série é estacionária.

#- processos estocstico. (Slide aula 06)
#- verificar se é estacionario ou não-estacionário.

autoplot(df_ts)
autoplot(acf(df_ts, plot=FALSE))
autoplot(pacf(df_ts, plot=FALSE))

# Raiz unitária + constante (no R = drift)
adf.drift <- ur.df(y = df_ts, type = c("drift"), lags = 1, selectlags = "AIC")
adf.drift

pnorm(1.28)

pnorm(1.65)

acf(adf.drift@res, lag.max=12)

# Raiz unitária + constante + tendência determinística (no R = trend)
adf_trend <- ur.df(y = df_ts, type = c("trend"), lags = 1, selectlags = "AIC")
adf_trend

summary(adf_trend)@teststat

summary(adf_trend)@cval

acf(adf_trend@res, lag.max=12)

#Portanto, a série temporal não ? estacionária, não rejeitamos a Hipótese Nula.

#**H0: A série é não estacionária.**
#-- dados transformados (Slide aula 06)
#- aplicar teste de linebox verifica se os residuos são iid
#Analisando o test Ljung-Box, vemos que o *p-value = 0,00000176*, sendo um valor muito abaixo de 1%, indício de dados são autocorrelacionados. Portanto rejeitamos Hipótese nula.

#**H1: Os resíduos não são i.i.d.;**
  
## 6 - Transformação das diferenças

#- aplicar tranformações: das diferenças. (Slide Aula 09)

df_ts_diff <- diff(df_ts)

# Teste de autocorrelação
lb_diff <- Box.test(df_ts_diff, type="Ljung-Box")
print(lb_diff)

#- construir a acf e a pacf.
autoplot(df_ts_diff)
autoplot(acf(df_ts_diff, plot=FALSE))
autoplot(pacf(df_ts_diff, plot=FALSE))

#- descobrir os parametros dos modelos.
#- parametros do modelo ar(p) e do ma(q).

#Estimação
#modelo  SARIMA(1,1,1)(1,1,1)12

#AR
fit.soja.ar <- Arima(df_ts, order = c(1,0,0), method = "ML", lambda = 0)
summary(fit.soja.ar)

#MA
fit.soja.ma <- Arima(df_ts, order = c(0,0,1), method = "ML", lambda = 0)
summary(fit.soja.ma)

#ARMA
fit.soja.arma <- Arima(df_ts, order = c(1,0,1), method = "ML", lambda = 0)
summary(fit.soja.arma)

#ARIMA
fit.soja.arima <- Arima(df_ts, order = c(1,1,1), method = "ML", lambda = 0)
summary(fit.soja.arima)


# Verificar se os parâmetros do modelo são significativos
# função de teste de significância dos parâmetros
t.test <- function(modelo_arima){
  # estatística t
  coef <- modelo_arima$coef
  se <- sqrt(diag(modelo_arima$var.coef))
  t <- abs(coef/se)
  # Teste t
  ok <- t > qt(0.975, length(modelo_arima$x) - sum(modelo_arima$arma[c(1,2,3,4,6,7)]))
  resul <- data.frame(Coef = coef, sd = se, t = t, rej_H0 = ok)
  return(resul)
}

# teste de significância para o modelo SARIMA(1,1,1)(1,1,1)12
t.test(fit.soja.ar)
t.test(fit.soja.ma)
t.test(fit.soja.arma)
t.test(fit.soja.arima)

#AIC (deu arima)
AIC(fit.soja.ar, fit.soja.ma, fit.soja.arma, fit.soja.arima)

#Previsão
diag <- tsdiag(fit.soja.arima, gof.lag = 20)
prev <- forecast(object = fit.soja.arima, h=6, level =0.95)
autoplot(prev)
accuracy(fit.soja.arima)
