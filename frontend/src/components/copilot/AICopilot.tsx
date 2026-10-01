import { useState, type ChangeEvent } from "react";
import { Send, Upload, Bot } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import type { RootState } from "../../store/store";

import {
  setDocument,
  setExtraction,
  setExtractionData,
  setAnalysis,
  setFormValues,
} from "../../store/deviationSlice";

import {
  extractDeviation,
  analyzeDeviation,
  uploadDocument,
} from "../../services/api";

export default function AICopilot() {
  const [message, setMessage] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const dispatch = useDispatch();

  const analysis = useSelector(
    (state: RootState) => state.deviation.analysis
  );

  const documentStatus = useSelector(
  (state: RootState) => state.deviation.document.status
    );

  const handleFileUpload = async (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file || isProcessing) {
      return;
    }

    try {
      setIsProcessing(true);

      dispatch(
        setDocument({
          file,
          status: "uploading",
          preview: "",
        })
      );

      const result = await uploadDocument(file);

      dispatch(
        setDocument({
          file,
          text: result.text,
          status: "uploaded",
          preview: result.text,
        })
      );

      dispatch(
        setExtraction({
          status: "processing",
          progress: 50,
          error: null,
        })
      );

      const extractedData = await extractDeviation(result.text);

      dispatch(setExtractionData(extractedData));

      dispatch(
        setExtraction({
          status: "complete",
          progress: 100,
        })
      );

      dispatch(setFormValues(extractedData));

      dispatch(
        setAnalysis({
          status: "processing",
        })
      );

      const analysis = await analyzeDeviation(extractedData);

      dispatch(
        setAnalysis({
          status: "complete",
          impact: analysis.impact,
          severity: analysis.severity,
        })
      );

      console.log("Uploaded document:", file.name);
      console.log("Extraction:", extractedData);
      console.log("Analysis:", analysis);
    } catch (error) {
      console.error("Document upload error:", error);

      dispatch(
        setDocument({
          status: "error",
        })
      );

      dispatch(
        setExtraction({
          status: "error",
          error: "Failed to process the uploaded document.",
        })
      );

      dispatch(
        setAnalysis({
          status: "error",
        })
      );
    } finally {
      setIsProcessing(false);

      // Allows selecting the same file again later.
      event.target.value = "";
    }
  };

  const handleSend = async () => {
    if (!message.trim() || isProcessing) {
      return;
    }

    try {
      setIsProcessing(true);

      dispatch(
        setDocument({
          text: message,
          status: "uploaded",
          preview: message,
        })
      );

      dispatch(
        setExtraction({
          status: "processing",
          progress: 50,
          error: null,
        })
      );

      const extractedData = await extractDeviation(message);

      dispatch(setExtractionData(extractedData));

      dispatch(
        setExtraction({
          status: "complete",
          progress: 100,
        })
      );

      dispatch(setFormValues(extractedData));

      dispatch(
        setAnalysis({
          status: "processing",
        })
      );

      const analysis = await analyzeDeviation(extractedData);

      dispatch(
        setAnalysis({
          status: "complete",
          impact: analysis.impact,
          severity: analysis.severity,
        })
      );

      setMessage("");

      console.log("Extraction:", extractedData);
      console.log("Analysis:", analysis);
    } catch (error) {
      console.error("AI Copilot error:", error);

      dispatch(
        setExtraction({
          status: "error",
          error: "Failed to process the deviation.",
        })
      );

      dispatch(
        setAnalysis({
          status: "error",
        })
      );
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="ai-copilot">
      <div className="copilot-header">
        <div className="copilot-title">
          <div className="copilot-icon">
            <Bot size={20} />
          </div>

          <div>
            <h2>AI Copilot</h2>
            <span>Deviation Intake Assistant</span>
          </div>
        </div>

        <div className="copilot-status">
          <span className="status-dot" />
          {isProcessing
  ? "Processing..."
  : documentStatus === "uploaded"
    ? "Document uploaded"
    : "Ready"}
        </div>
      </div>

      <div className="copilot-content">
        <div className="copilot-welcome">
          <div className="welcome-icon">
            <Bot size={24} />
          </div>

          <h3>How can I help?</h3>

          <p>
            Describe a deviation, ask for an update,
            or upload a document and I will extract
            the relevant information.
          </p>
        </div>

        {analysis.status === "complete" && (
          <div className="ai-assessment">
            <h3>AI Assessment</h3>

            <div className="assessment-item">
  <div className="assessment-label">
    <strong>Impact</strong>
    <span className="assessment-level">
      {analysis.impact.level ?? "Not assessed"}
    </span>
  </div>

  <p>{analysis.impact.reasoning}</p>
</div>

<div className="assessment-item">
  <div className="assessment-label">
    <strong>Severity</strong>
    <span className="assessment-level">
      {analysis.severity.level ?? "Not assessed"}
    </span>
  </div>

  <p>{analysis.severity.reasoning}</p>
</div>
          </div>
        )}

        <div className="copilot-examples">
          <button
            onClick={() =>
              setMessage(
                "A deviation occurred at the manufacturing plant involving a process parameter outside the approved range."
              )
            }
          >
            Describe a deviation
          </button>

          <button
            onClick={() =>
              setMessage(
                "Update the batch number and date of occurrence for the current deviation."
              )
            }
          >
            Edit deviation
          </button>
        </div>

        <div className="copilot-composer">
          <textarea
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Describe the deviation or ask the AI Copilot..."
            rows={4}
            disabled={isProcessing}
          />

          <div className="composer-actions">
            <label className="upload-button">
              <Upload size={17} />
              Upload Document

              <input
                type="file"
                accept=".pdf,.txt"
                hidden
                onChange={handleFileUpload}
              />
            </label>

            <button
              className="send-button"
              onClick={handleSend}
              disabled={!message.trim() || isProcessing}
            >
              <Send size={17} />
              {isProcessing ? "Processing..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}