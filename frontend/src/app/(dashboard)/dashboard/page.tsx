export default function DashboardPage() {

  return (

    <div>

      <h1 className="text-3xl font-bold">
        Dashboard
      </h1>


      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">


        <div className="border rounded-xl p-6">
          <h2 className="font-semibold">
            Resumes
          </h2>

          <p className="text-muted-foreground">
            Upload and optimize resumes
          </p>
        </div>



        <div className="border rounded-xl p-6">
          <h2 className="font-semibold">
            Jobs
          </h2>

          <p className="text-muted-foreground">
            Search and match jobs
          </p>
        </div>



        <div className="border rounded-xl p-6">
          <h2 className="font-semibold">
            AI Tools
          </h2>

          <p className="text-muted-foreground">
            Resume tailoring and cover letters
          </p>
        </div>


      </div>

    </div>

  );

}