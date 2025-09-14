const { Client } = require('pg')

const getData = async () => {
    try {
        const client = new Client({
            host: process.env.DB_HOST || 'localhost',
            port: 5432,
            database: 'demo',
            user: 'user',
            password: 'password',
        })
        await client.connect()

        const res = await client.query('SELECT * from articles')
        console.log(res.rows[0].title)
        await client.end()
    } catch (err) {
        console.error(err);
    }
}

module.exports = getData