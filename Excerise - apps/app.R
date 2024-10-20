library(shiny)
library(plotly)
source("datafeed.R")
source("helpers.R")


# user interface is defined here
ui <- fluidPage(
  titlePanel(h1("market betas vs. average returns")),
  
  sidebarLayout(
    sidebarPanel(
      h2("controls"),
      br(),
      selectInput("frequency",
                  label = "select frequency",
                  choices = list("daily" = "daily", 
                                 "monthly" = "monthly",
                                 "yearly" = "yearly"), selected = "daily"),
      br(),

      checkboxGroupInput("stock_selection", label = "Select Stocks to Include", choices = NULL),
      br(),
      
      p("data until:"),
      textOutput("last_date")
      
    ),
    
    mainPanel(
      h2("results"), 
      plotlyOutput("plot")
    )
  )
)

# what your computer/server does is defined here
server <- function(input, output, session) {
  # get data
  r <- get_stock_data()
  
  observe({updateCheckboxGroupInput(session, "stock_selection", choices = colnames(r), selected = colnames(r))})
  
  filtered_data <- reactive({
    req(input$stock_selection)
    r[, input$stock_selection, drop = FALSE]
  })
  
  # calculate betas based on data frequency
  inputB = reactive({
    calculate_betas(filtered_data(), freq = input$frequency, mkt_col = "SPY")
  })
  
  output$plot <- renderPlotly({
    # means
    mu = colMeans(filtered_data()) * 252 * 100
    # betas
    b = inputB()
    # both to data.frame
    df = data.frame(b, mu = mu)
    # ols fit
    fit <- lm(mu ~ b, data = df)
    
    # plot
    fig <- plot_ly(
      type = "scatter",
      x = b, y = mu,
      data = df, 
      mode = "markers",
      text = rownames(df),
      showlegend = FALSE,
      name = "stock")
    
    fig <- fig %>%
      add_lines(x = df$b, y = fitted(fit), name = "ols fit")
    
    fig
    
  })
  
  output$last_date = renderText(as.character(tail(index(r), 1)))
}

# run the app
shinyApp(ui = ui, server = server, options = list(port=3838))
