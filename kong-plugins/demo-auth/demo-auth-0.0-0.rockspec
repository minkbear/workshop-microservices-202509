package = "demo-auth"
version = "0.0-0"
supported_platforms = {"linux", "macosx"}
source = {
  url = "git://github.com/up1/kong-demo-auth",
  tag = "0.0"
}
description = {
  summary = "Demo",
  license = "MIT",
  homepage = "https://github.com/up1/kong-demo-auth",
  detailed = [[
      Demo
  ]]
}
dependencies = {
	"lua ~> 5.1"
}
build = {
  type = "builtin",
  modules = {
    ["kong.plugins.demo-auth.handler"] = "src/handler.lua",
    ["kong.plugins.demo-auth.schema"] = "src/schema.lua"
  }
}