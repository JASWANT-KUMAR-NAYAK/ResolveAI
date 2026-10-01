import DeviationForm from "./components/deviation/DeviationForm";
import AICopilot from "./components/copilot/AICopilot";

function App() {
  return (
    <div className="app">
      <header className="top-header">
        <div>
          <strong>ResolveAI</strong>
          <span> | Quality Management System</span>
        </div>

        <div>Deviation Intake</div>
      </header>

      <main className="main-layout">
        <section className="form-panel">
          <div className="panel-header">
            <div>
              <h1>Log Deviation</h1>
              <p>
                Use AI Copilot to capture and assess a deviation.
              </p>
            </div>
          </div>

          <DeviationForm />
        </section>

        <section className="copilot-panel">
          <AICopilot />
        </section>
      </main>
    </div>
  );
}

export default App;