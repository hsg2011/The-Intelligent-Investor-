using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace StockWeb.Controllers
{
    public class ApiController : Controller
    {
        private readonly HttpClient _api;

        // Inject the named HttpClient
        public ApiController(IHttpClientFactory httpFactory)
        {
            _api = httpFactory.CreateClient("Api");
        }

        // GET: /Api
        public async Task<IActionResult> Index()
        {
            var symbols = await _api.GetFromJsonAsync<List<string>>("symbols");
            return View(symbols);
        }

        // GET: /Api/Analyze?symbol=AAPL
        public async Task<IActionResult> Analyze(string symbol)
        {
            if (string.IsNullOrWhiteSpace(symbol))
                return RedirectToAction(nameof(Index));

            var result = await _api.GetFromJsonAsync<Dictionary<string,string>>($"analyze/{symbol}");
            ViewBag.Symbol = symbol.ToUpper();
            ViewBag.Recommendation = result?["recommendation"] ?? "No Data";
            return View();
        }
    }
}
