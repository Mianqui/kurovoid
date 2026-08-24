with open("templates/dashboard/base_dashboard.html", "r") as f:
    content = f.read()

# Let's add it before </ul></nav> in the sidebar
new_link = """
                    <li class="px-3 py-2 rounded-sm mb-0.5 last:mb-0 {% if request.resolver_match.url_name == 'configuracion' %}bg-slate-900{% endif %}">
                        <a class="block text-slate-200 hover:text-white truncate transition duration-150 {% if request.resolver_match.url_name == 'configuracion' %}hover:text-slate-200{% endif %}" href="{% url 'dashboard:configuracion' %}">
                            <div class="flex items-center">
                                <svg class="shrink-0 h-6 w-6" viewBox="0 0 24 24">
                                    <path class="fill-current {% if request.resolver_match.url_name == 'configuracion' %}text-indigo-500{% else %}text-slate-400{% endif %}" d="M19.714 14.7l-7.007 7.007-1.414-1.414 7.007-7.007c-.195-.495-.296-1.03-.296-1.586 0-2.761 2.239-5 5-5s5 2.239 5 5-2.239 5-5 5c-.556 0-1.09-.101-1.586-.296zM15 22h-2v-2h-2v-2h-2v-2H7v-2H5v-2H3v-2h2V8h2V6h2V4h2V2h2v2h2v2h2v2h2v2h2v2h-2v2h-2v2h-2v2h-2v2z" />
                                </svg>
                                <span class="text-sm font-medium ml-3 duration-200">Configuración</span>
                            </div>
                        </a>
                    </li>
"""
content = content.replace("</ul>\n            </div>", new_link + "</ul>\n            </div>")

with open("templates/dashboard/base_dashboard.html", "w") as f:
    f.write(content)
