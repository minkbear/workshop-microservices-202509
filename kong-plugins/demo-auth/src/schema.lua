local typedefs = require "kong.db.schema.typedefs"

return {
  name = "demo-auth",
  fields = {
    {
      config = {
        type = "record",
        fields = {
          { url = { type = "string", required = true } },
          { connect_timeout = { type = "number", default = 10000 } },
          { send_timeout = { type = "number", default = 60000 } },
          { read_timeout = { type = "number", default = 60000 } },
        },
      },
    },
  },
}