index_js = """const express = require('express')

const healthRouter = require('./routes/api/health')

const app = express()
const port = '3000'

app.use('/api/health', healthRouter)
app.listen(port, () => {
  console.log(`Listening on ${port}`)
})
  
module.exports = app
"""

health_js = """const router = require('express').Router()

/* GET health */
router.get('/', async (req, res) => {
  res.json({
    message:'Project started with Honey',
    alive:true
    })
  })
  
module.exports = router 
"""