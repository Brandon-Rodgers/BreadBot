protected void doPut(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
    PeriodicLogger.shared.requestCount++;
    
    emWrap(() -> {
        if (Main.isShuttingDown()) {
            LoggingManager.println("Request from " + request.getRemoteAddr() + " while shutting down");
            response.sendError(StatusCode.SHUTTING_DOWN.getValue());
            return;
        }

        long beforeTime = System.nanoTime();
        String ip = null;
        String purpose = null;
        String requestString = null;
        JSONObject responseJson = new JSONObject();

        try {
            ip = request.getRemoteAddr();
            String compressedRequest = request.getReader().lines()
                    .collect(Collectors.joining(System.lineSeparator()));
            requestString = GZipTool.unzipToStr(Base64.getDecoder().decode(compressedRequest));

            JSONObject requestJson = new JSONObject(requestString);
            purpose = requestJson.optString("purpose");

            if (purpose.isEmpty()) {
                response.sendError(StatusCode.BAD_REQUEST.getValue());
                loggingManager.logError("User made PUT request without an included purpose", StatusCode.BAD_REQUEST,
                        requestString, responseJson.toString(), null, ip, getPath(), null);
                return;
            }

            APIStatus status = handleUnverifiedRequest(requestString, requestJson, responseJson, ip, purpose);
            if (status.isErr()) {
                response.setHeader("reason", status.getMessage());
                response.sendError(status.getStatusCode().getValue(), status.getMessage());
                return;
            }
            StatusCode statusCode = globalParams.handleGlobalParams(requestJson, responseJson);
            if (statusCode != StatusCode.OK) {
                response.sendError(statusCode.getValue());
                return;
            }

            response.setContentType("application/json");
            response.setStatus(StatusCode.OK.getValue());

            String compressedResponse = Base64.getEncoder().encodeToString(GZipTool.zip(responseJson.toString()));
            response.getWriter().println(compressedResponse);

            loggingManager.logSuccess("Successful unverified request", StatusCode.OK, requestString,
                    responseJson.toString(), null, ip, getPath(), purpose);

            double time = (System.nanoTime() - beforeTime) / 1000000.0;
            addRequestTime(time, getPath(), purpose);
            LoggingManager.println("Unverified request processing time: " + time + "ms \n");
        } catch (JSONException e1) {
            try {
                StringWriter sw = new StringWriter();
                e1.printStackTrace(new PrintWriter(sw));
                response.sendError(StatusCode.BAD_REQUEST.getValue());
                loggingManager.logError(sw.toString(), StatusCode.BAD_REQUEST, requestString,
                        responseJson.toString(), null, ip, getPath(), purpose);
            } catch (Exception e2) {
                e2.printStackTrace();
            }
        } catch (Exception e) {
            try {
                StringWriter sw = new StringWriter();
                e.printStackTrace(new PrintWriter(sw));
                response.sendError(StatusCode.UNKNOWN.getValue());
                loggingManager.logError(sw.toString(), StatusCode.UNKNOWN, requestString, responseJson.toString(),
                        null, ip, getPath(), purpose);
            } catch (Exception e2) {
                e2.printStackTrace();
            }
        }
    });
}