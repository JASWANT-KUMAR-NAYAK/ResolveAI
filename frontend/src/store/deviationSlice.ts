import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

import type {
  AnalysisState,
  DeviationData,
  DeviationIntakeState,
  DocumentState,
  ExtractionState,
} from "../types/deviation";

const emptyDeviationData: DeviationData = {
  site: "",
  dateOfOccurrence: "",
  title: "",
  description: "",
  relatedProduct: null,
  relatedMaterial: null,
  batchNumber: null,
  processParameter: null,
};

const initialState: DeviationIntakeState = {
  document: {
    file: null,
    text: "",
    status: "idle",
    preview: "",
  },

  extraction: {
    status: "idle",
    progress: 0,
    data: emptyDeviationData,
    confidence: 0,
    error: null,
  },

  analysis: {
    status: "idle",

    impact: {
      level: null,
      reasoning: "",
    },

    severity: {
      level: null,
      reasoning: "",
    },
  },

  form: {
    values: emptyDeviationData,
    isDirty: false,
    userEdits: {},
  },
};

const deviationSlice = createSlice({
  name: "deviation",
  initialState,

  reducers: {
    setDocument(
      state,
      action: PayloadAction<Partial<DocumentState>>,
    ) {
      state.document = {
        ...state.document,
        ...action.payload,
      };
    },

    setExtraction(
      state,
      action: PayloadAction<Partial<ExtractionState>>,
    ) {
      state.extraction = {
        ...state.extraction,
        ...action.payload,
      };
    },

    setExtractionData(
      state,
      action: PayloadAction<DeviationData>,
    ) {
      state.extraction.data = action.payload;
    },

    setAnalysis(
      state,
      action: PayloadAction<Partial<AnalysisState>>,
    ) {
      state.analysis = {
        ...state.analysis,
        ...action.payload,
      };
    },

    setFormValues(
      state,
      action: PayloadAction<DeviationData>,
    ) {
      state.form.values = action.payload;
      state.form.isDirty = false;
      state.form.userEdits = {};
    },

    updateFormValues(
      state,
      action: PayloadAction<Partial<DeviationData>>,
    ) {
      state.form.values = {
        ...state.form.values,
        ...action.payload,
      };

      state.form.isDirty = true;

      state.form.userEdits = {
        ...state.form.userEdits,
        ...action.payload,
      };
    },

    resetDeviation() {
      return initialState;
    },
  },
});

export const {
  setDocument,
  setExtraction,
  setExtractionData,
  setAnalysis,
  setFormValues,
  updateFormValues,
  resetDeviation,
} = deviationSlice.actions;

export default deviationSlice.reducer;