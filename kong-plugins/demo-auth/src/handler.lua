local http = require "resty.http"

local plugin = {
  PRIORITY = 900,
  VERSION = "1.0.0",
}

function plugin:access(conf)
  local client = http.new()
  client:set_timeouts(conf.connect_timeout, conf.send_timeout, conf.read_timeout)

  local res, err = client:request_uri(conf.url, {
    method = kong.request.get_method(),
    -- path = kong.request.get_path(),
    query = kong.request.get_raw_query(),
    headers = kong.request.get_headers(),
    body = kong.request.get_raw_body()
  })
  kong.log.debug("Print http response body")

  if not res then
    return kong.response.error(500, err and err.message or "Unknown error")
  end

  if res.status ~= 200 then
    return kong.response.error(res.status, res.body)
  end
end

return plugin