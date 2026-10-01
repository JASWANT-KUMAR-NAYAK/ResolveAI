import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import type { RootState } from "../../store/store";
import { updateFormValues } from "../../store/deviationSlice";
import { saveDeviation } from "../../services/api";

export default function DeviationForm() {
  const dispatch = useDispatch();

  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");

  const formValues = useSelector(
    (state: RootState) => state.deviation.form.values
  );

  const analysis = useSelector(
    (state: RootState) => state.deviation.analysis
  );

  const userEdits = useSelector(
    (state: RootState) => state.deviation.form.userEdits
  );

  const handleChange = (
    field: keyof typeof formValues,
    value: string
  ) => {
    dispatch(
      updateFormValues({
        [field]: value,
      })
    );
  };

  const handleSave = async () => {
    if (
      !formValues.site ||
      !formValues.dateOfOccurrence ||
      !formValues.title ||
      !formValues.description
    ) {
      setSaveMessage(
        "Please complete all required fields before saving."
      );
      return;
    }

    try {
      setIsSaving(true);
      setSaveMessage("");

      const result = await saveDeviation(
        formValues,
        analysis.impact,
        analysis.severity,
        userEdits
      );

      setSaveMessage(
        `Deviation saved successfully. ID: ${result.id}`
      );
    } catch (error) {
      console.error("Save error:", error);
      setSaveMessage("Failed to save deviation.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="deviation-form">
      <div className="form-section">
        <h2>Deviation Details</h2>

        <div className="form-grid">
          <div className="form-field">
            <label htmlFor="site">Site / Plant *</label>
            <input
              id="site"
              value={formValues.site}
              onChange={(event) =>
                handleChange("site", event.target.value)
              }
              placeholder="Site / Plant"
            />
          </div>

          <div className="form-field">
            <label htmlFor="dateOfOccurrence">
              Date of Occurrence *
            </label>
            <input
              id="dateOfOccurrence"
              type="date"
              value={formValues.dateOfOccurrence}
              onChange={(event) =>
                handleChange(
                  "dateOfOccurrence",
                  event.target.value
                )
              }
            />
          </div>

          <div className="form-field full-width">
            <label htmlFor="title">
              Title / Short Description *
            </label>
            <input
              id="title"
              value={formValues.title}
              onChange={(event) =>
                handleChange("title", event.target.value)
              }
              placeholder="Enter deviation title"
            />
          </div>

          <div className="form-field full-width">
            <label htmlFor="description">
              Detailed Description *
            </label>
            <textarea
              id="description"
              value={formValues.description}
              onChange={(event) =>
                handleChange("description", event.target.value)
              }
              placeholder="Detailed deviation description"
              rows={6}
            />
          </div>

          <div className="form-field">
            <label htmlFor="relatedProduct">
              Related Product
            </label>
            <input
              id="relatedProduct"
              value={formValues.relatedProduct ?? ""}
              onChange={(event) =>
                handleChange(
                  "relatedProduct",
                  event.target.value
                )
              }
              placeholder="Optional"
            />
          </div>

          <div className="form-field">
            <label htmlFor="relatedMaterial">
              Related Material
            </label>
            <input
              id="relatedMaterial"
              value={formValues.relatedMaterial ?? ""}
              onChange={(event) =>
                handleChange(
                  "relatedMaterial",
                  event.target.value
                )
              }
              placeholder="Optional"
            />
          </div>

          <div className="form-field">
            <label htmlFor="batchNumber">
              Batch / Lot Number
            </label>
            <input
              id="batchNumber"
              value={formValues.batchNumber ?? ""}
              onChange={(event) =>
                handleChange(
                  "batchNumber",
                  event.target.value
                )
              }
              placeholder="Optional"
            />
          </div>

          <div className="form-field">
            <label htmlFor="processParameter">
              Process Parameter Affected
            </label>
            <input
              id="processParameter"
              value={formValues.processParameter ?? ""}
              onChange={(event) =>
                handleChange(
                  "processParameter",
                  event.target.value
                )
              }
              placeholder="Optional"
            />
          </div>
        </div>
      </div>

      <div className="form-actions">
        <button
          type="button"
          onClick={handleSave}
          disabled={isSaving}
        >
          {isSaving ? "Saving..." : "Save Deviation"}
        </button>

        {saveMessage && (
           <div className="save-message">
    {saveMessage}
  </div>
        )}
      </div>
    </div>
  );
}